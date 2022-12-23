#pragma once

#include <regex>
#include <sstream>
#include <string>
#include <vector>

#include <pybind11/stl.h>

size_t utf8_strlen(const char *begin, const char *end);
std::vector<char *> to_argv(const std::vector<std::string> &arguments);
std::string escape(const std::string &text);