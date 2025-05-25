import pytest
import os

import core.typecast
import core.functions

def test_typecast():
	assert core.typecast.typeCast("123") == 123
	assert core.typecast.typeCast("123.456") == 123.456
	assert core.typecast.typeCast("null") == None
	assert core.typecast.typeCast("true") == True
	assert core.typecast.typeCast("false") == False
	assert core.typecast.typeCast("[1,2]") == [1, 2]
	assert core.typecast.typeCast("[1,\"2\"]") == [1, "2"]
	assert core.typecast.typeCast("{\"key\": \"value\"}") == {"key": "value"}

def test_typecast_dynamic():
	assert core.typecast.dynamic("data[event][test]",{ "data" : { "event" : { "test" : 123 } } }) == 123
	def testFunction():
		return "testFunction"
	core.functions.available["testFunction"] = testFunction
	assert core.typecast.dynamic("testFunction()") == "testFunction"

def test_typecast_flatten():
	assert core.typecast.flatten({ "test" : { "test1" : { "test2" : 123 } } }) == {	"test.test1.test2": 123 }

def test_typecast_getField():
	assert core.typecast.getField("data[event][test]", { "test" : 123 }) == 123