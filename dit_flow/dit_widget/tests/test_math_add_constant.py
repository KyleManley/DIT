from dit_flow.dit_widget.math_add_constant import math_add_constant


def test_math_add_constant(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write("1.00\n'2.00'\n'-999.99'\n'4.00'\n0A\n0B\n")
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    math_add_constant(1.0, -999.99, log_file='{}'.format(temp_log_file.strpath),
                      output_data_file='{}'.format(temp_out_file.strpath),
                      input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '2.00\n3.00\n-999.99\n5.00\n-999.99\n-999.99'
    expected_log = 'Adding 1.0 to the column\n'\
                   '    Records with non-number entry types:\n'\
                   '         Record                Value\n'\
                   '              5                   0A\n'\
                   '              6                   0B\n'\
                   '    Total number of non-number entries: 2\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
