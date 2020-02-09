# ---------------------------------------- #
# BottomRight : なるべく下の方の右端に置く #
# ---------------------------------------- #
use strict;
use utf8;

my $BLANK = 0;
my $BLACK = 1;
my $WHITE = -1;

# 標準入力取得
my $color = <STDIN>;
my $size = <STDIN>;
chomp $color;
chomp $size;

my @board = ();
for (my $i=0; $i<$size; $i++) {
    my $tmp = <STDIN>;
    chomp $tmp;
    my @row = split /\s+/, $tmp;
    push @board, [@row];
}

print STDERR "$color\n";
print STDERR "$size\n";
foreach my $row (@board) {
    print STDERR join " ", @$row, "\n";
}

# 置ける場所の一番下の右端を返す
my @possibles = &get_possibles($color, $size, \@board);
print STDERR join(" , ", @possibles) . "\n";

print($possibles[0]);


# 石が置ける場所をすべて返す
sub get_possibles {
    my ($color, $size, $r_board) = @_;
    my @possibles = ();

    foreach my $y (reverse(0..$size-1)) {
        foreach my $x (reverse(0..$size-1)) {
            if (&is_reversible($color, $size, $r_board, $x, $y) > 0) {
                push @possibles, "$x $y";
            }
        }
    }

    return @possibles;
}

# 石をひっくり返せるか判定する
sub is_reversible {
    my ($color, $size, $r_board, $x, $y) = @_;
    my $ret = 0;

    # 方向
    # (-1,  1) (0,  1) (1,  1)
    # (-1,  0)         (1,  0)
    # (-1, -1) (0, -1) (1, -1)
    my $directions = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]];

    # 石が置かれていない
    if ($$r_board[$y][$x] == $BLANK) {
        # 8方向をチェック
        foreach my $dxdy (@$directions) {
            my ($next_x, $next_y) = ($x, $y);
            my $tmp = 0;
            while (1) {
                ($next_x, $next_y) = ($next_x + $$dxdy[0], $next_y + $$dxdy[1]);

                # 座標が範囲内
                if ($next_x >=0 and $next_x < $size and $next_y >=0 and $next_y < $size) {
                    my $next_value = $$r_board[$next_y][$next_x];

                    # 石が置かれている
                    if ($next_value != $BLANK) {
                        # 置いた石と同じ色が置かれている
                        if ($next_value == $color) {
                            last;
                        }

                        $tmp++;
                    }
                    else {
                        $tmp = 0;
                        last;
                    }
                }
                else {
                    $tmp = 0;
                    last;
                }
            }

            $ret += $tmp;
        }
    }

    return $ret;
}

__END__
