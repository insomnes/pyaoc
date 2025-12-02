from librarium.modclock import CountMode, CrossingPositionTracker, ModClock, PositionTracker


class TestPositionTracker:
    def test_advance(self):
        tracker = PositionTracker(start=0, modulus=10, to_look_up=0)
        tracker.advance(5)
        assert tracker.cur == 5
        assert tracker.counter == 0

        tracker.advance(5)
        assert tracker.cur == 0
        assert tracker.counter == 1

    def test_regress(self):
        tracker = PositionTracker(start=5, modulus=10, to_look_up=0)
        tracker.regress(3)
        assert tracker.cur == 2
        assert tracker.counter == 0

        tracker.regress(2)
        assert tracker.cur == 0
        assert tracker.counter == 1


class TestCrossingPositionTracker:
    def test_advance(self):
        tracker = CrossingPositionTracker(start=0, modulus=10, to_look_up=0)
        tracker.advance(25)
        assert tracker.cur == 5
        assert tracker.counter == 2

        tracker.advance(5)
        assert tracker.cur == 0
        assert tracker.counter == 3

    def test_regress(self):
        tracker = CrossingPositionTracker(start=5, modulus=10, to_look_up=0)
        tracker.regress(15)
        assert tracker.cur == 0
        assert tracker.counter == 2

        tracker.regress(10)
        assert tracker.cur == 0
        assert tracker.counter == 3

        tracker.regress(5)
        assert tracker.cur == 5
        assert tracker.counter == 3


class TestModClock:
    def test_exact_counting(self):
        clock = ModClock.from_parameters(
            start=50,
            modulus=100,
            count_mode=CountMode.EXACT,
            to_look_up=0,
        )
        moves = [-68, -30, 48, -5, 60, -55, -1, -99, 14, -82]
        expected_counter = 3
        clock.make_moves(moves)
        assert clock.counter == expected_counter

    def test_crossing_counting(self):
        clock = ModClock.from_parameters(
            start=50,
            modulus=100,
            count_mode=CountMode.CROSSING,
            to_look_up=0,
        )
        moves = [-68, -30, 48, -5, 60, -55, -1, -99, 14, -82]
        expected_counter = 6
        clock.make_moves(moves)
        assert clock.counter == expected_counter
