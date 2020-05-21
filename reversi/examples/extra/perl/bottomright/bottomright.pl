# ---------------------------------------------------------------- #
# BottomRight : Put it on the lower right edge as much as possible #
# ---------------------------------------------------------------- #
use strict;
use utf8;

my $BLANK = 0;
my $BLACK = 1;
my $WHITE = -1;

# Get STDIN
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

# Returns the bottom right edge of the available space
my @legal_moves = &get_legal_moves($color, $size, \@board);
print STDERR join(" , ", @legal_moves) . "\n";

print($legal_moves[0]);


# Return all places where discs can be placed
sub get_legal_moves {
    my ($color, $size, $r_board) = @_;
    my @legal_moves = ();

    foreach my $y (reverse(0..$size-1)) {
        foreach my $x (reverse(0..$size-1)) {
            if (&is_reversible($color, $size, $r_board, $x, $y) > 0) {
                push @legal_moves, "$x $y";
            }
        }
    }

    return @legal_moves;
}

# Determine if you can turn the stone over
sub is_reversible {
    my ($color, $size, $r_board, $x, $y) = @_;
    my $ret = 0;

    # (-1,  1) (0,  1) (1,  1)
    # (-1,  0)         (1,  0)
    # (-1, -1) (0, -1) (1, -1)
    my $directions = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]];

    if ($$r_board[$y][$x] == $BLANK) {
        foreach my $dxdy (@$directions) {
            my ($next_x, $next_y) = ($x, $y);
            my $tmp = 0;
            while (1) {
                ($next_x, $next_y) = ($next_x + $$dxdy[0], $next_y + $$dxdy[1]);

                if ($next_x >=0 and $next_x < $size and $next_y >=0 and $next_y < $size) {
                    my $next_value = $$r_board[$next_y][$next_x];

                    if ($next_value != $BLANK) {
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
