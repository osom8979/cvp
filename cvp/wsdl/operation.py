# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Annotated, Any, List, Optional, Tuple

from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Operation
from zeep.xsd import Element
from zeep.xsd.elements.any import Any as ZeepAny
from zeep.xsd.types.builtins import default_types

from cvp.inspect.argument import Argument, ArgumentMapper
from cvp.logging.logging import wsdl_logger as logger
from cvp.resources.formats.json import JsonFormatPath
from cvp.types import override
from cvp.wsdl.schema import XsdSchema
from cvp.wsdl.serialize import serialize_object


class WsdlOperationProxy(OperationProxy):
    def __init__(
        self,
        jsons: JsonFormatPath,
        uuid: str,
        binding_name: str,
        operation_name: str,
        service_proxy: ServiceProxy,
        operation: Operation,
        schema: Optional[XsdSchema] = None,
    ):
        super().__init__(service_proxy, operation_name)
        self._uuid = uuid
        self._jsons = jsons
        self._binding_name = binding_name
        self._operation = operation

        input_elements = self._operation.input.body.type.elements
        self._arguments = self._create_arguments(input_elements, schema)
        self._latest = None

    @staticmethod
    def _create_arguments(
        input_elements: List[Tuple[str, Element]],
        schema: Optional[XsdSchema] = None,
    ):
        result = ArgumentMapper()
        for name, element in input_elements:
            kind = Parameter.POSITIONAL_OR_KEYWORD
            default = Parameter.empty
            value = Parameter.empty
            assert isinstance(element.type.accepted_types, list)
            assert isinstance(element.type.attributes, list)

            if element.type.qname:
                builtin_type = default_types.get(element.type.qname)
                if builtin_type is not None:
                    type_info = builtin_type
                elif schema is not None:
                    type_name = type(element.type).__name__
                    try:
                        type_info = schema.get_type(type_name)
                    except KeyError:
                        type_info = schema.elements.get(type_name)
                else:
                    type_info = None
            else:
                assert isinstance(element, ZeepAny)
                type_info = None

            if element.type.accepted_types:
                primary_accepted_type = element.type.accepted_types[0]
            else:
                primary_accepted_type = Any
            assert isinstance(primary_accepted_type, type)

            _T = primary_accepted_type
            annotation = Annotated[_T, type_info]  # type: ignore[valid-type]
            result[name] = Argument.from_details(name, kind, default, annotation, value)
        return result

    @property
    def input_elements(self) -> List[Tuple[str, Element]]:
        return self._operation.input.body.type.elements

    @property
    def arguments(self):
        return self._arguments

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def binding_name(self) -> str:
        return self._binding_name

    @property
    def name(self) -> str:
        assert isinstance(self._op_name, str)
        return self._op_name

    @property
    def latest(self) -> Any:
        return self._latest

    @latest.setter
    def latest(self, value: Any) -> None:
        self._latest = value

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        return self.uuid, self.binding_name, self.name

    def has_latest(self) -> bool:
        return self._latest is not None

    def has_cache(self) -> bool:
        return self._jsons.has_object(*self.cache_args)

    def read_cache(self) -> Any:
        return self._jsons.read_object(*self.cache_args)

    def write_cache(self, o: Any) -> int:
        return self._jsons.write_object(o, *self.cache_args)

    def remove_cache(self) -> None:
        self._jsons.remove_object(*self.cache_args)

    def clear_latest(self) -> None:
        self._latest = None

    @override
    def __call__(self, *args, **kwargs):
        prefix = f"Call {self.name}(args={args}, kwargs={kwargs})"

        if self._latest is not None:
            logger.info(f"{prefix} memory cache")
        elif self.has_cache():
            logger.info(f"{prefix} file cache")
            self._latest = self.read_cache()
        else:
            logger.info(f"{prefix} operation")
            response = super().__call__(*args, **kwargs)
            self._latest = serialize_object(response)
            self.write_cache(self._latest)

        return self._latest

    def call_with_arguments(self):
        return self.__call__(**self._arguments.kwargs())
