import pytest
import os
from main import Importer, Visualizer

@pytest.fixture
def sample_input_file(tmp_path):
    file_content = """Lenzing, 170447112, 34.75, EUR, Vienna;
                      Andritz, 170447131, 59.41, USD, New York;
                      EVN, 170447132, 28.55, EUR, Vienna;
                      EVN, 170447133, 31.18, USD, New York;"""
    file_path = tmp_path / "sample_input.txt"
    with open(file_path, 'w') as f:
        f.write(file_content)
    return file_path

def test_importer_read(sample_input_file):
    importer = Importer(str(sample_input_file), 'output.csv')
    data = importer.read()

    assert len(data) == 4
    assert data[0] == "Lenzing, 170447112, 34.75, EUR, Vienna;\n"

def test_importer_transform(sample_input_file, tmp_path):
    output_file_path = tmp_path / "output.csv"
    importer = Importer(str(sample_input_file), str(output_file_path))
    transformed_data = importer.transform()

    assert transformed_data
    assert os.path.exists(str(output_file_path))

    with open(output_file_path, 'r') as f:
        output_content = f.read()
        assert "COMPANY,DATE,SHARE,CURRENCY,COMPANY_LOCATION\n" in output_content
        assert "LENZING,1975-05-27 18:25:12,34.75,EUR,VIENNA\n" in output_content

def test_visualizer_export(sample_input_file, tmp_path):
    output_visualization_path = tmp_path / "visualization.jpg"
    visualizer = Visualizer(str(sample_input_file))
    visualizer.export()

    assert os.path.exists('visualization/image.jpg')