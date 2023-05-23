# Project Structure

src
    This folder contains *all* the source code of this distribution.

src/expressions
    Root package of this distribution. All source code is a module or subpackage of expressions.

    
tests
    Test folder. All the test code lives here. Notice that for test work properly, this distribution must have been
    installed. It's recommended to install this distribution in development mode (see README).

tests/unit
    Unit test package. All tests in this package *must* be unitary: they must test only code in this distribution. In
    particular, unit tests *must not* depend on external components, like DBMS, web servers, or any external
    application. Unit tests must be fast, and the test suite must run under a few seconds. This package should
    follow the same module structure than expressions.

tests/integration
    Integration test package. The purpose of integration tests is to test the interoperation of the current distribution
    with external components, like DBMS, web servers, or any external application. Every external dependency *must* be
    run locally.

docs
    Documentation folder.

docs/adr
    Folder for Architectural Decision Records. Every ADR must reside in its own file.

docs/build
    This folder contains the documents built from the rst or markdown sources.

scripts
    This folder contain helpful scripts required to build the project, its docker image, and deployment. *NO application
    code* should reside in this folder.
