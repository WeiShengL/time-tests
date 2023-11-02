from times import compute_overlap_time, time_range
import pytest

def test_generic_case():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]
    assert compute_overlap_time(large, short) == expected

def test_no_overlap():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-12-12 12:30:00", "2010-12-12 12:45:00")
    expected = "Time range does not overlap"
    assert compute_overlap_time(large, short) == [expected]

def test_several_intervals():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2, 60)
    short = time_range("2010-01-12 10:30:00", "2010-01-12 14:30:00", 2, 60)
    expected = [("2010-01-12 10:30:00", "2010-01-12 10:59:30"), "Time range does not overlap", ("2010-01-12 11:00:30", "2010-01-12 12:00:00"), "Time range does not overlap"]
    assert compute_overlap_time(large, short) == expected

@pytest.mark.parametrize("start_input1, end_input1, number_of_intervals_input1, gap_between_intervals_s_input1, start_input2, end_input2, number_of_intervals_input2, gap_between_intervals_s_input2, expected", 
                         [("2010-01-12 10:00:00", "2010-01-12 12:00:00", 1, 0, "2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60, [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")])],
                        #  [("2010-01-12 10:00:00", "2010-01-12 12:00:00", 1, 0, "2010-12-12 12:30:00", "2010-12-12 12:45:00", 1, 0, ["Time range does not overlap"])]
                         )
def test_general(start_input1, end_input1, number_of_intervals_input1, gap_between_intervals_s_input1, start_input2, end_input2, number_of_intervals_input2, gap_between_intervals_s_input2, expected):
    large = time_range(start_input1, end_input1, number_of_intervals_input1, gap_between_intervals_s_input1)
    short = time_range(start_input2, end_input2, number_of_intervals_input2, gap_between_intervals_s_input2)
    assert compute_overlap_time(large, short) == expected


def test_time_backwards():
    error_msg = "Start time must be before end time"
    with pytest.raises(ValueError, match=error_msg):
        time_range("2010-01-12 10:00:00", "2010-01-12 08:00:00") 