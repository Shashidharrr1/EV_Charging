from setuptools import setup, find_packages

setup(
    name="ev_recharge",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'mysql-connector-python',
        'python-dotenv',
        'PyJWT'  # Add JWT package
    ],
)