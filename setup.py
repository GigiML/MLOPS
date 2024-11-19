from setuptools import setup, find_packages

setup(
    name='sentiment_analyzer',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={"":"src"},    
    install_requires=[
        'click',  
        'pandas', 
        'mlflow', 
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'predict=sentiment_analyser.predict:main',
            'promote=sentiment_analyser.promote:main'
        ],
    },
)