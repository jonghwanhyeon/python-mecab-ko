#include "utils.h"

// Reference: https://stackoverflow.com/a/4063229
size_t utf8_strlen(const char *begin, const char *end) {
  size_t length = 0;
  for (const char *iterator = begin; iterator < end; iterator += 1) {
    length += ((*iterator & 0xC0) != 0x80);
  }
  return length;
}

std::vector<char *> to_argv(const std::vector<std::string> &arguments) {
  std::vector<char *> argv{const_cast<char *>("")}; // argv[0] is excutable name
  for (const auto &argument : arguments) {
    argv.push_back(const_cast<char *>(argument.c_str()));
  }
  return argv;
}

std::string escape(const std::string &text) {
  std::regex pattern("([\"\\\\])");
  return std::regex_replace(text, pattern, "\\$1");
}