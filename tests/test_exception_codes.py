import json
import unittest
from enum import IntEnum
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.testclient import TestClient

from basalam.backbone_api.exceptions.client_error import (
    BadRequestException, PaymentRequiredException, TooManyRequestsException,
    ClientErrorException, ConflictException, ErrorDetail, ForbiddenException,
    NotFoundException, UnauthorizedException, UnprocessableEntityException,
)
from basalam.backbone_api.exceptions.client_error.handlers import client_error_exception_handler


class ApplicationCode(IntEnum):
    EXAMPLE = 42203


class ExceptionCodeTests(unittest.TestCase):
    def cases(self, **kwargs):
        return [
            (ClientErrorException(400, **kwargs), 400),
            (BadRequestException(**kwargs), 400),
            (PaymentRequiredException(**kwargs), 402),
            (TooManyRequestsException(**kwargs), 429),
            (UnauthorizedException(**kwargs), 401),
            (ForbiddenException(**kwargs), 403),
            (NotFoundException(**kwargs), 404),
            (ConflictException([{'id': 123}], **kwargs), 409),
            (UnprocessableEntityException('Required', ['campaign_id'], **kwargs), 422),
        ]

    def test_existing_calls_keep_default_zero(self):
        for exception, status in self.cases():
            with self.subTest(exception=type(exception).__name__):
                self.assertEqual(exception.status_code, status)
                self.assertEqual(exception.errors[0].code, 0)

    def test_custom_codes_reach_http_responses(self):
        for code in (42203, ApplicationCode.EXAMPLE, 0):
            for exception, status in self.cases(code=code):
                with self.subTest(exception=type(exception).__name__, code=code):
                    app = FastAPI()
                    app.add_exception_handler(ClientErrorException, client_error_exception_handler)

                    @app.get('/error')
                    async def error():
                        raise exception

                    with TestClient(app) as client:
                        response = client.get('/error')
                    self.assertEqual(response.status_code, status)
                    body = response.json()
                    self.assertEqual(body['http_status'], status)
                    self.assertEqual(body['errors'][0]['code'], int(code))
                    self.assertIs(type(body['errors'][0]['code']), int)
                    if status == 409:
                        self.assertEqual(body['data'], [{'id': 123}])
                    if status == 422:
                        self.assertEqual(body['errors'][0]['fields'], ['campaign_id'])
                        self.assertEqual(body['errors'][0]['message'], 'Required')

    def test_messages_and_legacy_positional_arguments_preserved(self):
        for cls in (UnauthorizedException, ForbiddenException, NotFoundException):
            for message in (None, '', 'Custom message'):
                with self.subTest(exception=cls.__name__, message=message):
                    old = cls(message)
                    new = cls(message, code=123)
                    self.assertEqual(new.message, old.message)
                    self.assertEqual(new.detail, old.detail)
                    self.assertEqual(new.errors[0].message, old.errors[0].message)
                    self.assertEqual(new.errors[0].code, 123)
                    self.assertEqual(new.message, message or HTTPStatus(new.http_status).phrase)
        conflict = ConflictException([{'id': 1}], 'Duplicate', code=40901)
        self.assertEqual(conflict.errors[0].data, [{'id': 1}])
        self.assertEqual(conflict.errors[0].message, 'Duplicate')
        invalid = UnprocessableEntityException('Invalid', ['amount'], code=42211)
        self.assertEqual(invalid.errors[0].fields, ['amount'])

    def test_optional_fields_and_data_with_custom_code(self):
        exception = UnprocessableEntityException('Required', code=42203)
        response = client_error_exception_handler(None, exception)
        self.assertEqual(json.loads(response.body)['errors'][0]['code'], 42203)
        # Preserve the constructor's acceptance of None. The existing conflict
        # response model requires a list, so HTTP callers still pass [] or data.
        conflict = ConflictException(None, code=40901)
        self.assertIsNone(conflict.errors[0].data)
        self.assertEqual(conflict.errors[0].code, 40901)

    def test_current_message_behavior_is_unchanged(self):
        exception = ForbiddenException('Reason is not accessible', code=40304)
        body = json.loads(client_error_exception_handler(None, exception).body)
        self.assertEqual(body['message'], 'Reason is not accessible')
        self.assertEqual(body['errors'][0]['message'], 'Reason is not accessible')
        self.assertEqual(body['http_status'], 403)

    def test_explicit_details_take_precedence_and_are_not_mutated(self):
        errors = [ErrorDetail(code=10, message='First'), ErrorDetail(code=20, message='Second')]
        exception = ClientErrorException(400, errors, code=99)
        self.assertIs(exception.errors, errors)
        self.assertEqual([error.code for error in exception.errors], [10, 20])
        body = json.loads(client_error_exception_handler(None, exception).body)
        self.assertEqual([error['code'] for error in body['errors']], [10, 20])
        empty = []
        self.assertIs(ClientErrorException(400, empty, code=99).errors, empty)

    def test_code_is_keyword_only(self):
        for cls, args in (
            (ClientErrorException, (400, None)),
            (BadRequestException, ('message', [])),
            (PaymentRequiredException, ('message', [])),
            (TooManyRequestsException, ('message', [])),
            (UnauthorizedException, ('message',)),
            (ForbiddenException, ('message',)),
            (NotFoundException, ('message',)),
            (ConflictException, (None, 'message')),
            (UnprocessableEntityException, ('message', [])),
        ):
            with self.subTest(exception=cls.__name__):
                with self.assertRaises(TypeError):
                    cls(*args, 123)

    def test_new_exceptions_preserve_wallet_detail_fields(self):
        for cls, status in (
            (BadRequestException, 400),
            (PaymentRequiredException, 402),
            (TooManyRequestsException, 429),
        ):
            for fields in (None, [], ['amount']):
                for message in (None, '', 'Custom message'):
                    with self.subTest(exception=cls.__name__, fields=fields, message=message):
                        exception = cls(message, fields, code=123)
                        response = client_error_exception_handler(None, exception)
                        body = json.loads(response.body)
                        self.assertEqual(response.status_code, status)
                        self.assertEqual(body['http_status'], status)
                        self.assertEqual(body['message'], message or HTTPStatus(status).phrase)
                        self.assertEqual(body['errors'], [{
                            'code': 123, 'message': message, 'fields': fields, 'data': None,
                        }])

    def test_new_exception_and_response_exports(self):
        from basalam.backbone_api import exceptions, responses
        from basalam.backbone_api.responses import client_error
        for exception in (BadRequestException, PaymentRequiredException, TooManyRequestsException):
            with self.subTest(exception=exception.__name__):
                self.assertIs(getattr(exceptions, exception.__name__), exception)
                self.assertIn(exception.__name__, exceptions.__all__)
                name = exception.__name__.replace('Exception', 'Response')
                self.assertIs(getattr(responses, name), getattr(client_error, name))
                self.assertIn(name, responses.__all__)

    def test_new_response_models_default_to_their_http_status(self):
        from basalam.backbone_api.responses import BadRequestResponse, PaymentRequiredResponse, TooManyRequestsResponse
        for model, status in ((BadRequestResponse, 400), (PaymentRequiredResponse, 402), (TooManyRequestsResponse, 429)):
            with self.subTest(model=model.__name__):
                response = model(message='Custom', errors=[{'code': 123, 'fields': ['amount']}]).as_json_response()
                self.assertEqual(response.status_code, status)
                self.assertEqual(json.loads(response.body)['http_status'], status)
                schema = model.model_json_schema()
                self.assertIn('fields', schema['$defs']['DetailedError']['properties'])


if __name__ == '__main__':
    unittest.main()
