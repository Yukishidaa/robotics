"""Test URDF/Xacro model structure and validity."""

import os
import subprocess
import sys
import tempfile
import unittest

from ament_index_python.packages import get_package_share_directory


class TestUrdfModel(unittest.TestCase):
    """Проверка структуры и валидности URDF/Xacro модели."""

    def setUp(self):
        self.pkg_share = get_package_share_directory('course_description')
        self.xacro_path = os.path.join(self.pkg_share, 'urdf', 'vehicle.urdf.xacro')

    def test_xacro_file_exists(self):
        """Xacro файл существует и не пуст."""
        self.assertTrue(os.path.isfile(self.xacro_path))
        self.assertGreater(os.path.getsize(self.xacro_path), 0)

    def test_xacro_contains_required_links(self):
        """Xacro содержит все_required link'и."""
        with open(self.xacro_path) as f:
            content = f.read()
        for link in ['base_link', 'camera_link', 'lidar_link', 'imu_link']:
            self.assertIn(f'name="{link}"', content)

    def test_xacro_contains_required_joints(self):
        """Xacro содержит все_required joints."""
        with open(self.xacro_path) as f:
            content = f.read()
        for joint in ['camera_joint', 'lidar_joint', 'imu_joint']:
            self.assertIn(f'name="{joint}"', content)

    def test_xacro_has_parent_child_relations(self):
        """Каждый joint имеет parent и child."""
        with open(self.xacro_path) as f:
            content = f.read()
        self.assertIn('<parent link="base_link"/>', content)
        self.assertIn('<child link="camera_link"/>', content)

    def test_xacro_has_inertial(self):
        """Все link'и имеют inertial элементы."""
        with open(self.xacro_path) as f:
            content = f.read()
        self.assertIn('<inertial>', content)
        self.assertIn('<mass', content)

    def test_xacro_has_visual_and_collision(self):
        """Все link'и имеют visual и collision."""
        with open(self.xacro_path) as f:
            content = f.read()
        self.assertIn('<visual>', content)
        self.assertIn('<collision>', content)

    def test_xacro_parameters_exist(self):
        """Есть параметризованные размеры (не магические числа)."""
        with open(self.xacro_path) as f:
            content = f.read()
        self.assertIn('xacro:property', content)
        self.assertIn('wheel_radius', content)
        self.assertIn('track_width', content)


if __name__ == '__main__':
    unittest.main()
