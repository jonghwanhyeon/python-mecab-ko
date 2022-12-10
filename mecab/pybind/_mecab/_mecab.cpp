#include <pybind11/pybind11.h>

namespace py = pybind11;

void initialize_cli(py::module &m);
void initialize_dictionaryinfo(py::module &m);
void initialize_lattice(py::module &m);
void initialize_node(py::module &m);
void initialize_path(py::module &m);
void initialize_tagger(py::module &m);

PYBIND11_MODULE(_mecab, m) {
  initialize_cli(m);
  initialize_dictionaryinfo(m);
  initialize_lattice(m);
  initialize_node(m);
  initialize_path(m);
  initialize_tagger(m);
}