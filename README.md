# sports-scheduling

## Environment

[Conda](https://conda.io/) is used as the package, dependency and environment manager. The dependencies of the application are defined in
the file `environment.yml`

The Conda environment can be set up using `environment.yml`:

```bash
conda env create -f environment.yml
```

After creating the environment, configure the Python Interpreter to use the new environment. In PyCharm (as of v2021.2.3), go to
`Settings` > `Python Interpreter` and Click the setting gear icon besides the Python Interpreter drop down list.
The `Add Python Interpreter` window should pop up.  
Navigate to `Conda Enviornment` in the left-hand side > Check `Existing environment` and choose the executable interpreter from the
environment path you just created.


