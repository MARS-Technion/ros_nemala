from setuptools import setup

package_name = 'ros_nemala'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David Dovrat',
    maintainer_email='ddovrat@cs.technion.ac.il',
    description='A ROS2 version of NEMALA/tools',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'node_manager = ros_nemala.node_manager:main'
        ],
    },
)
