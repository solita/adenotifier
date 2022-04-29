import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='adenotifier',
    version='0.1.0',
    author='Taha Gad, Henri Hemminki',
    author_email='taha.gad@solita.fi, henri.hemminki@solita.fi',
    description='Python library for using ADE Notify API',
    url='https://github.com/solita-internal/ade-notifier',
    project_urls = {
        "Bug Tracker": "https://github.com/solita-internal/ade-notifier/issues"
    },
    license='MIT',
    packages=['adenotifier'],
    py_modules=['manifest', 'notifier'],
    install_requires=['requests']
)