# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Annotated, Any, List, Optional, Tuple

from zeep.proxy import OperationProxy, ServiceProxy
from zeep.wsdl.definitions import Operation
from zeep.xsd import Element
from zeep.xsd.types.builtins import default_types

from cvp.inspect.argument import Argument, ArgumentMapper
from cvp.resources.subdirs.pickles import Pickles
from cvp.types import override
from cvp.wsdl.schema import XsdSchema


class WsdlOperationProxy(OperationProxy):
    def __init__(
        self,
        pickles: Pickles,
        uuid: str,
        binding_name: str,
        operation_name: str,
        service_proxy: ServiceProxy,
        operation: Operation,
        schema: Optional[XsdSchema] = None,
    ):
        super().__init__(service_proxy, operation_name)
        self._uuid = uuid
        self._pickles = pickles
        self._binding_name = binding_name
        self._operation = operation

        input_elements = self._operation.input.body.type.elements
        self._arguments = self._create_arguments(input_elements, schema)

    @staticmethod
    def _create_arguments(
        input_elements: List[Tuple[str, Element]],
        schema: Optional[XsdSchema] = None,
    ):
        result = ArgumentMapper()
        for name, element in input_elements:
            kind = Parameter.POSITIONAL_OR_KEYWORD
            default = None
            value = None
            assert isinstance(element.type.accepted_types, list)
            assert 1 <= len(element.type.accepted_types)
            assert isinstance(element.type.attributes, list)

            builtin_type = default_types.get(element.type.qname)
            if builtin_type is not None:
                type_info = builtin_type
            elif schema is not None:
                is_complex_type = bool(element.type.attributes)
                element_type_name = type(element.type).__name__

                if is_complex_type:
                    type_info = schema.complex_types[element_type_name]
                else:
                    type_info = schema.simple_types[element_type_name]
                    # TODO: KeyError: 'TimeZone'
            else:
                type_info = None

            primary_accepted_type = element.type.accepted_types[0]
            assert isinstance(primary_accepted_type, type)
            annotation = Annotated[primary_accepted_type, type_info]
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
    def cache_args(self) -> Tuple[str, str, str]:
        return self.uuid, self.binding_name, self.name

    def has_cache(self) -> bool:
        return self._pickles.has_object(*self.cache_args)

    def read_cache(self) -> Any:
        return self._pickles.read_object(*self.cache_args)

    def write_cache(self, o: Any) -> int:
        return self._pickles.write_object(o, *self.cache_args)

    @override
    def __call__(self, *args, **kwargs):
        if self.has_cache():
            return self.read_cache()
        else:
            response = super().__call__(*args, **kwargs)
            self.write_cache(response)
            return response

    def call_with_arguments(self):
        return self.__call__(**self._arguments.kwargs())
