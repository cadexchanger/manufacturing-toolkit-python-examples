# CAD Exchanger MTK examples in Python

This repository contains examples for CAD Exchanger Manufacturing Toolkit (MTK) utilizing the Python API.

More information about CAD Exchanger MTK can be found [here](https://cadexchanger.com/products/sdk/add-ons/manufacturing-toolkit/). You can find overview of available examples and a brief summary for each one [here](https://docs.cadexchanger.com/mtk/mtk_examples_page.html).

The examples are provided under a permissive Modified BSD License. You may insert their source code into your application and modify as needed.

## Requirements

* Latest version of CAD Exchanger SDK
* Latest version of CAD Exchanger MTK
* CPython 3.8 - 3.10

## Running

To use the examples, first obtain the CAD Exchanger MTK evaluation [here](https://cadexchanger.com/contact-us/licensing-inquiry/). Please describe your use case in detail. Upon filling out the form you'll receive an email with an evaluation license key for SDK (`cadex_license.lic` file) and MTK (`mtk_license.lic` file). There will also be links to the pip repositories containing the CAD Exchanger SDK and MTK packages.

1. Install the CAD Exchanger SDK package with the following command, substituting `<repo-sdk-link-from-email>` for the actual link to pip repository:

    ```
    $ pip install cadexchanger --extra-index-url=<repo-sdk-link-from-email>
    ```

2. Install the CAD Exchanger MTK package with the following command, substituting `<repo-mtk-link-from-email>` for the actual link to pip repository:

    ```
    $ pip install manufacturingtoolkit --extra-index-url=<repo-mtk-link-from-email>
    ```
    
3. Place the license keys into the repository root.

4. Then navigate to your example of choice and launch it with the following command:

    ```
    $ python dfm/sheet_metal_analyzer/run.py
    ```

    Every `run.py` script first generates a runtime key specific to the sample being launched and then runs the sample with pre-packaged models.

    Learn more about runtime keys and SDK licensing starting from CAD Exchanger 3.18 [here](https://docs.cadexchanger.com/sdk/sdk_licensing.html).

5. Once the `run.py` script has been used at least once and runtime license key is available, you can try out the sample with custom parameters. For example, for `sheet_metal_analyzer` sample, substitute `<input-model>` for your CAD model that you want to convert:

    ```
    $ python dfm/sheet_metal_analyzer/sheet_metal_analyzer.py <input-model>
    ```

    It's also possible to copy the runtime key creation code from `run.py` to the sample's main source file and use the sample directly right away.

## Learn more

If you'd like to learn more about CAD Exchanger, visit our [website](https://cadexchanger.com/). If you have any questions, please reach out to us [here](https://cadexchanger.com/contact-us/).
