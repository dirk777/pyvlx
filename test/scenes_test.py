"""Unit test for Scenes object."""
import unittest
from unittest.mock import patch
import asyncio
import json

from pyvlx import PyVLX, Scenes, Scene, PyVLXException


# pylint: disable=too-many-public-methods,invalid-name
class TestScenes(unittest.TestCase):
    """Test class for scenes object."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_get_item(self):
        """Test get_item from Scene object."""
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)

        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        scene2 = Scene(pyvlx, 1, 'Scene_2')
        scenes.add(scene2)
        scene3 = Scene(pyvlx, 2, 'Scene_3')
        scenes.add(scene3)
        scene4 = Scene(pyvlx, 3, 'Scene_4')
        scenes.add(scene4)

        self.assertEqual(scenes['Scene_1'], scene1)
        self.assertEqual(scenes['Scene_2'], scene2)
        self.assertEqual(scenes['Scene_3'], scene3)
        self.assertEqual(scenes['Scene_4'], scene4)

        self.assertEqual(scenes[0], scene1)
        self.assertEqual(scenes[1], scene2)
        self.assertEqual(scenes[2], scene3)
        self.assertEqual(scenes[3], scene4)

    def test_get_item_failed(self):
        """Test get_item with non existing object."""
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)
        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        with self.assertRaises(KeyError):
            scenes['Scene_2']  # pylint: disable=pointless-statement
        with self.assertRaises(IndexError):
            scenes[1]  # pylint: disable=pointless-statement

    def test_iter(self):
        """Test iterator."""
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)

        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        scene2 = Scene(pyvlx, 1, 'Scene_2')
        scenes.add(scene2)
        scene3 = Scene(pyvlx, 2, 'Scene_3')
        scenes.add(scene3)
        scene4 = Scene(pyvlx, 3, 'Scene_4')
        scenes.add(scene4)

        self.assertEqual(
            tuple(scenes.__iter__()),
            (scene1, scene2, scene3, scene4))

    def test_len(self):
        """Test len()."""
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)
        self.assertEqual(len(scenes), 0)
        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        self.assertEqual(len(scenes), 1)

        scene2 = Scene(pyvlx, 1, 'Scene_2')
        scenes.add(scene2)
        self.assertEqual(len(scenes), 2)

        scene3 = Scene(pyvlx, 2, 'Scene_3')
        scenes.add(scene3)
        self.assertEqual(len(scenes), 3)

        scene4 = Scene(pyvlx, 3, 'Scene_4')
        scenes.add(scene4)
        self.assertEqual(len(scenes), 4)

    def test_add_item_failed(self):
        """Test add() with wrong type."""
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)
        with self.assertRaises(TypeError):
            scenes.add(scenes)
        with self.assertRaises(TypeError):
            scenes.add("scenes")

    def test_load_windows(self):
        """Test load windows."""
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)

        get_response = \
            '{"token":"aEGjV20T32j1V3EJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name":"All windows closed","id":0,"sil' + \
            'ent":false,"products":[{"typeId":4,"name":"Window 1","actuat' + \
            'or":0,"status":0},{"typeId":4,"name":"Window 2","actuator":0' + \
            ',"status":0}]},{"name":"All windows open","id":1,"silent":fa' + \
            'lse,"products":[{"typeId":4,"name":"Window 1","actuator":0,"' + \
            'status":100},{"typeId":4,"name":"Window 2","actuator":0,"sta' + \
            'tus":100}]}],"errors":[]}'

        scenes.data_import(json.loads(get_response))

        self.assertEqual(len(scenes), 2)
        self.assertEqual(scenes[0], Scene(pyvlx, 0, 'All windows closed'))
        self.assertEqual(scenes[1], Scene(pyvlx, 1, 'All windows open'))

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call(self, mock_apicall):
        """Test if interface is called correctly."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)
        get_response = \
            '{"token":"aEGjV20T32j1V3EJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name":"All windows closed","id":0,"sil' + \
            'ent":false,"products":[{"typeId":4,"name":"Window 1","actuat' + \
            'or":0,"status":0},{"typeId":4,"name":"Window 2","actuator":0' + \
            ',"status":0}]},{"name":"All windows open","id":1,"silent":fa' + \
            'lse,"products":[{"typeId":4,"name":"Window 1","actuator":0,"' + \
            'status":100},{"typeId":4,"name":"Window 2","actuator":0,"sta' + \
            'tus":100}]}],"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        self.loop.run_until_complete(asyncio.Task(
            scenes.load()))
        mock_apicall.assert_called_with('scenes', 'get')
        self.assertEqual(len(scenes), 2)
        self.assertEqual(scenes[0], Scene(pyvlx, 0, 'All windows closed'))
        self.assertEqual(scenes[1], Scene(pyvlx, 1, 'All windows open'))

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call_failed(self, mock_apicall):
        """Test if error is raised if no data element is in response."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)
        get_response = \
            '{"token":"aEGjV20T32j1V3EJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        with self.assertRaises(PyVLXException):
            self.loop.run_until_complete(asyncio.Task(
                scenes.load()))


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestScenes)
unittest.TextTestRunner(verbosity=2).run(SUITE)
