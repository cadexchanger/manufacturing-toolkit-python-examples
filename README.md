# Manufacturing Toolkit examples in Python

This repository contains examples for Manufacturing Toolkit (MTK) utilizing the Python API.

More information about MTK can be found [here](https://cadexchanger.com/products/sdk/add-ons/manufacturing-toolkit/). You can find overview of available examples and a brief summary for each one [here](https://docs.cadexchanger.com/mtk/mtk_examples_page.html).

The examples are provided under a permissive Modified BSD License. You may insert their source code into your application and modify as needed.

## Requirements

* Latest version of CAD Exchanger SDK
* Latest version of Manufacturing Toolkit
* Windows x86-64: CPython 3.7 - 3.11
* Linux x86-64: CPython 3.7 - 3.11
* macOS Apple Silicon: Python 3.7 - 3.11

## Running

To use the examples, first obtain the MTK evaluation [here](https://cadexchanger.com/contact-us/licensing-inquiry/). Please describe your use case in detail. Upon filling out the form you'll receive an email with an evaluation license key for SDK (`cadex_license.py` file) and MTK (`mtk_license.py` file). There will also be links to the pip repository containing the CAD Exchanger SDK and MTK packages. You can also register in our [Customer Corner](https://my.cadexchanger.com/) and see both the license key and the repository link there.

1. Install the CAD Exchanger SDK package with the following command, substituting `<repo-link-from-email>` for the actual link to pip repository:

    ```
    $ pip install cadexchanger --extra-index-url=<repo-link-from-email>
    ```

    If you get an error message that `pip` was not able to find the package, please check the requirements above and make sure that your configuration is supported.

2. Install the MTK package with the following command, substituting `<repo-link-from-email>` for the actual link to pip repository:

    ```
    $ pip install manufacturingtoolkit --extra-index-url=<repo-link-from-email>
    ```

    If you get an error message that `pip` was not able to find the package, please check the requirements above and make sure that your configuration is supported.

3. Place the license keys into the repository root.

4. Then navigate to your example of choice and launch it with the following command:

    ```
    $ python dfm/sheet_metal_analyzer/run.py
    ```

5. You can also launch each sample with custom parameters. For example, for `sheet_metal_analyzer` sample, substitute `<input-model>` for your CAD model that you want to convert:

    ```
    $ python dfm/sheet_metal_analyzer/sheet_metal_analyzer.py <input-model>
    ```

    To find out which parameters each sample requires, either launch it without parameters, or view the source code.

## Learn more

If you'd like to learn more about CAD Exchanger, visit our [website](https://cadexchanger.com/). If you have any questions, please reach out to us [here](https://cadexchanger.com/contact-us/).
