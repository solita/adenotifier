
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ade_notifier',
    version='0.0.1',
    author='Taha Gad, Henri Hemminki',
    author_email='taha.gad@solita.fi, henri.hemminki@solita.fi',
    description='Python library for using ADE Notify API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/solita-internal/ade-notifier',
    project_urls = {
        "Bug Tracker": "https://github.com/solita-internal/ade-notifier/issues"
    },
    license='MIT',
    packages=['ade_notifier'],
    install_requires=['requests']
)