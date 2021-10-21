# DigitalUni homework aggregator

This tool connects to a DigitalUni account and lists all homework currently
assigned to its user.

[DigitalUni](https://campus.sfc.unistra.fr/) is a learning platform of the
university of Strasbourg that centralises every information and interaction for
a training course. The user interface lacks a lot of quality-of-life features,
one of the worst problems being that homework assignment information is
scattered over all the lesson pages and there is no aggregated view.

## How to use

First, write the login and password of a DigitalUni account in `credentials.yml`
following the format of `credentials_example.yml`. You can then generate an HTML
file that displays the homework by calling the `aggregator.py` script.

There also is a raw text output but it won't be available until options handling
is implemented, see
[issue #7](https://github.com/Dettorer/digitaluni-homework-aggregator/issues/7).

### Using pip

```shell
pip install -r requirements.txt
./aggregator.py output.html
```

### Using nix

```shell
nix-shell
./aggregator.py output.html
```

### Using nix with direnv

```shell
echo "use_nix" > .direnvrc
direnv allow
./aggregator.py output.html
```
