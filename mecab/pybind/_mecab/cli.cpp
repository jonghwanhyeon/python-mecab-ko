#include <mecab.h>
#include <pybind11/pybind11.h>

#include "utils.h"

namespace py = pybind11;

void initialize_cli(py::module &m) {
  py::module m_cli = m.def_submodule("cli");

  m_cli.def("mecab", [](const std::vector<std::string> &arguments) {
    std::vector<char *> argv = to_argv(arguments);
    return mecab_do(argv.size(), argv.data());
  });

  m_cli.def("dict_index", [](const std::vector<std::string> &arguments) {
    std::vector<char *> argv = to_argv(arguments);
    return mecab_dict_index(argv.size(), argv.data());
  });

  m_cli.def("dict_gen", [](const std::vector<std::string> &arguments) {
    std::vector<char *> argv = to_argv(arguments);
    return mecab_dict_gen(argv.size(), argv.data());
  });

  m_cli.def("cost_train", [](const std::vector<std::string> &arguments) {
    std::vector<char *> argv = to_argv(arguments);
    return mecab_cost_train(argv.size(), argv.data());
  });
}