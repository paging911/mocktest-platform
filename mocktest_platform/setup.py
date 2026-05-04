from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().splitlines()

setup(
    name="mocktest_platform",
    version="0.0.1",
    description="Mock test platform custom app for Frappe / ERPNext LMS",
    author="Custom",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)

