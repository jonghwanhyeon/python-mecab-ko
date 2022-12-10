#include "utils.h"

std::vector<char *> to_argv(const std::vector<std::string> &arguments) {
  std::vector<char *> argv{""}; // argv[0] is excutable name
  for (const auto &argument : arguments) {
    argv.push_back(const_cast<char *>(argument.c_str()));
  }
  return argv;
}

std::string escape(const std::string &text) {
  std::regex pattern("([\"\\\\])");
  return std::regex_replace(text, pattern, "\\$1");
}