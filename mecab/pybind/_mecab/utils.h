#pragma once

#include <regex>
#include <sstream>
#include <string>
#include <vector>

#include <pybind11/stl.h>

std::vector<char *> to_argv(const std::vector<std::string> &arguments);
std::string escape(const std::string &text);