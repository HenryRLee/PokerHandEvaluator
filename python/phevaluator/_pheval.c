/*
 *  Copyright 2016-2023 Henry Lee
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

/*
 * Python C extension exposing the native PH Evaluator functions.
 *
 * It is a thin wrapper around the C implementation found in the sibling
 * `cpp/` directory, so the Python package evaluates hands using the exact
 * same algorithm and tables as the C/C++ library.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <phevaluator/phevaluator.h>

static PyObject *pheval_evaluate_5cards(PyObject *self, PyObject *args) {
  int a, b, c, d, e;
  if (!PyArg_ParseTuple(args, "iiiii", &a, &b, &c, &d, &e)) {
    return NULL;
  }
  return PyLong_FromLong(evaluate_5cards(a, b, c, d, e));
}

static PyObject *pheval_evaluate_6cards(PyObject *self, PyObject *args) {
  int a, b, c, d, e, f;
  if (!PyArg_ParseTuple(args, "iiiiii", &a, &b, &c, &d, &e, &f)) {
    return NULL;
  }
  return PyLong_FromLong(evaluate_6cards(a, b, c, d, e, f));
}

static PyObject *pheval_evaluate_7cards(PyObject *self, PyObject *args) {
  int a, b, c, d, e, f, g;
  if (!PyArg_ParseTuple(args, "iiiiiii", &a, &b, &c, &d, &e, &f, &g)) {
    return NULL;
  }
  return PyLong_FromLong(evaluate_7cards(a, b, c, d, e, f, g));
}

static PyObject *pheval_evaluate_omaha_cards(PyObject *self, PyObject *args) {
  int c1, c2, c3, c4, c5, h1, h2, h3, h4;
  if (!PyArg_ParseTuple(args, "iiiiiiiii", &c1, &c2, &c3, &c4, &c5, &h1, &h2,
                        &h3, &h4)) {
    return NULL;
  }
  return PyLong_FromLong(
      evaluate_omaha_cards(c1, c2, c3, c4, c5, h1, h2, h3, h4));
}

static PyObject *pheval_evaluate_plo4_cards(PyObject *self, PyObject *args) {
  int c1, c2, c3, c4, c5, h1, h2, h3, h4;
  if (!PyArg_ParseTuple(args, "iiiiiiiii", &c1, &c2, &c3, &c4, &c5, &h1, &h2,
                        &h3, &h4)) {
    return NULL;
  }
  return PyLong_FromLong(
      evaluate_plo4_cards(c1, c2, c3, c4, c5, h1, h2, h3, h4));
}

#ifdef PHEVALUATOR_HAVE_PLO5
static PyObject *pheval_evaluate_plo5_cards(PyObject *self, PyObject *args) {
  int c1, c2, c3, c4, c5, h1, h2, h3, h4, h5;
  if (!PyArg_ParseTuple(args, "iiiiiiiiii", &c1, &c2, &c3, &c4, &c5, &h1, &h2,
                        &h3, &h4, &h5)) {
    return NULL;
  }
  return PyLong_FromLong(
      evaluate_plo5_cards(c1, c2, c3, c4, c5, h1, h2, h3, h4, h5));
}
#endif  // PHEVALUATOR_HAVE_PLO5

#ifdef PHEVALUATOR_HAVE_PLO6
static PyObject *pheval_evaluate_plo6_cards(PyObject *self, PyObject *args) {
  int c1, c2, c3, c4, c5, h1, h2, h3, h4, h5, h6;
  if (!PyArg_ParseTuple(args, "iiiiiiiiiii", &c1, &c2, &c3, &c4, &c5, &h1, &h2,
                        &h3, &h4, &h5, &h6)) {
    return NULL;
  }
  return PyLong_FromLong(
      evaluate_plo6_cards(c1, c2, c3, c4, c5, h1, h2, h3, h4, h5, h6));
}
#endif  // PHEVALUATOR_HAVE_PLO6

static PyMethodDef pheval_methods[] = {
    {"evaluate_5cards", pheval_evaluate_5cards, METH_VARARGS,
     "Evaluate 5 cards and return their rank (1 is the strongest)."},
    {"evaluate_6cards", pheval_evaluate_6cards, METH_VARARGS,
     "Evaluate the best 5 of 6 cards and return their rank."},
    {"evaluate_7cards", pheval_evaluate_7cards, METH_VARARGS,
     "Evaluate the best 5 of 7 cards and return their rank."},
    {"evaluate_omaha_cards", pheval_evaluate_omaha_cards, METH_VARARGS,
     "Evaluate an Omaha hand (5 community + 4 hole cards) and return its rank."},
    {"evaluate_plo4_cards", pheval_evaluate_plo4_cards, METH_VARARGS,
     "Evaluate a PLO4 hand (5 community + 4 hole cards) and return its rank."},
#ifdef PHEVALUATOR_HAVE_PLO5
    {"evaluate_plo5_cards", pheval_evaluate_plo5_cards, METH_VARARGS,
     "Evaluate a PLO5 hand (5 community + 5 hole cards) and return its rank."},
#endif  // PHEVALUATOR_HAVE_PLO5
#ifdef PHEVALUATOR_HAVE_PLO6
    {"evaluate_plo6_cards", pheval_evaluate_plo6_cards, METH_VARARGS,
     "Evaluate a PLO6 hand (5 community + 6 hole cards) and return its rank."},
#endif  // PHEVALUATOR_HAVE_PLO6
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef pheval_module = {
    PyModuleDef_HEAD_INIT,
    "_pheval",
    "Native PH Evaluator bindings backed by the C/C++ library.",
    -1,
    pheval_methods,
};

PyMODINIT_FUNC PyInit__pheval(void) {
  return PyModule_Create(&pheval_module);
}
