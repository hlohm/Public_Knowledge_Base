---
type: cheatsheet
area: "Programming Languages"
aliases: []
tags: [perl, programming, regex, text-processing, one-liners]
status: working
---

# Perl

> **Area:** [[Programming Languages]]

Perl's strongest suit is text processing: powerful regex, one-liners for log munging, and quick scripts for transforming data. This sheet covers that 80% — one-liners, regex, and practical idioms.

---

## 1. One-liners

The `-e`, `-n`, `-p`, `-i`, `-a` flags make Perl a command-line text processing tool.

```sh
# Print lines matching a pattern
perl -ne 'print if /ERROR/' logfile.txt

# Print non-matching lines (like grep -v)
perl -ne 'print unless /DEBUG/' logfile.txt

# Substitute in-place (like sed -i, but more powerful)
perl -pi -e 's/foo/bar/g' file.txt

# In-place with backup
perl -pi.bak -e 's/foo/bar/g' file.txt

# Auto-split on delimiter (-a sets @F; -F sets delimiter)
perl -F: -ane 'print "$F[0]\n"' /etc/passwd   # print usernames

# Sum a column
perl -ane '$sum += $F[2]; END { print "$sum\n" }' data.txt

# Print line numbers with content
perl -ne 'printf "%4d: %s", $., $_' file.txt   # $. = line number

# Print lines 5 through 10
perl -ne 'print if $. >= 5 && $. <= 10' file.txt

# Remove duplicate adjacent lines (like uniq)
perl -ne 'print unless $_ eq $prev; $prev = $_'

# Strip trailing whitespace
perl -pi -e 's/\s+$/\n/' file.txt

# Double-space a file (insert blank line after each)
perl -pe '$_ .= "\n"' file.txt

# Count occurrences of a pattern
perl -lne '$n++ if /pattern/; END { print $n }' file.txt

# Extract and print a captured group
perl -ne 'print "$1\n" if /User: (\S+)/' logfile.txt
```

## 2. Regex

Perl's regex is the gold standard — most modern regex engines derive from it.

```perl
# Match
if ($str =~ /pattern/) { ... }
if ($str !~ /pattern/) { ... }    # negated match

# Match and capture
if ($str =~ /(\d{4})-(\d{2})-(\d{2})/) {
    my ($year, $month, $day) = ($1, $2, $3);
}

# Named captures (Perl 5.10+)
if ($str =~ /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/) {
    print "$+{year}-$+{month}-$+{day}\n";
}

# Global match — collect all matches
my @emails = ($text =~ /[\w.+-]+@[\w-]+\.[a-z]{2,}/gi);
my $count  = () = $text =~ /pattern/g;   # count matches

# Substitution
$str =~ s/old/new/;          # first occurrence
$str =~ s/old/new/g;         # global
$str =~ s/foo/bar/gi;        # case-insensitive, global
$str =~ s/^\s+|\s+$//g;      # trim whitespace

# Substitution with code (e modifier)
$str =~ s/(\d+)/$1 * 2/ge;  # double every number in the string

# Modifiers
/pattern/i    # case-insensitive
/pattern/g    # global
/pattern/m    # ^ and $ match line boundaries
/pattern/s    # . matches \n
/pattern/x    # allow whitespace and comments in regex
```

## 3. Variables and data types

```perl
# Scalars
my $name = "Alice";
my $num  = 42;
my $pi   = 3.14;
my $flag = 1;         # true (non-zero, non-empty)

# Strings
my $s = "Hello, $name";       # interpolates variables
my $s = 'No $interpolation';  # single-quotes are literal
my $s = qq{Hello, $name};     # like double-quotes
my $s = q{No $interpolation}; # like single-quotes

# String operations
length($s), index($s, "sub"), substr($s, 0, 5)
uc($s), lc($s), ucfirst($s), lcfirst($s)
chomp $s;           # remove trailing \n
chop $s;            # remove last character
reverse $s          # reverse string

# Arrays
my @arr = (1, 2, 3, "four");
$arr[0]             # 1
$arr[-1]            # last: "four"
scalar @arr         # 4 (length)
push @arr, 5;       # append
pop @arr;           # remove and return last
unshift @arr, 0;    # prepend
shift @arr;         # remove and return first
my @slice = @arr[1..3];                 # slice

# Array operations
my @sorted = sort { $a <=> $b } @arr;   # numeric sort
my @rsort  = reverse sort @arr;          # reversed
my @unique = do { my %seen; grep { !$seen{$_}++ } @arr };
join(", ", @arr)
split(/,\s*/, $str)
grep { /pattern/ } @arr    # filter
map  { uc $_ } @arr        # transform

# Hashes
my %h = (name => "Alice", age => 30);
$h{name}                   # "Alice"
$h{city} //= "Unknown";    # defined-or: set if undefined
keys %h, values %h
delete $h{name};
exists $h{name}            # true if key exists

# Reference and dereference
my $aref = [1, 2, 3];     # anonymous array ref
my $href = {a => 1};       # anonymous hash ref
$aref->[0]                 # 1
$href->{a}                 # 1
push @{$aref}, 4;          # dereference to push
```

## 4. Control flow

```perl
# if / elsif / else
if ($x > 0) {
    ...
} elsif ($x == 0) {
    ...
} else {
    ...
}

# Postfix (for short guards)
print "positive\n" if $x > 0;
next if /^#/;               # skip comments

# unless (like if not)
print "zero\n" unless $x;

# Loops
for my $i (1..10) { print "$i\n"; }
foreach my $item (@arr) { print "$item\n"; }
while ($line = <STDIN>) { chomp $line; ... }

# Loop controls
next;    # continue (like Python continue)
last;    # break (like Python break)
redo;    # restart current iteration without re-evaluating condition

# C-style for
for (my $i = 0; $i < 10; $i++) { ... }
```

## 5. File I/O

```perl
# Open and read
open(my $fh, '<', 'file.txt') or die "Cannot open: $!";
while (my $line = <$fh>) {
    chomp $line;
    ...
}
close $fh;

# Slurp entire file
open(my $fh, '<', 'file.txt') or die $!;
my @lines = <$fh>;    # array of lines
# or: my $content = do { local $/; <$fh> };
close $fh;

# Write
open(my $fh, '>', 'out.txt')  or die $!;   # overwrite
open(my $fh, '>>', 'out.txt') or die $!;   # append
print $fh "Hello\n";
close $fh;
```

## 6. Subroutines

```perl
sub greet {
    my ($name, $greeting) = @_;    # always unpack @_ at the start
    $greeting //= "Hello";
    return "$greeting, $name!";
}

print greet("Alice");               # Hello, Alice!
print greet("Alice", "Hi");         # Hi, Alice!

# Named parameters via hash
sub connect {
    my (%args) = @_;
    my $host = $args{host} // 'localhost';
    my $port = $args{port} // 5432;
    ...
}
connect(host => 'db.example.com', port => 5433);
```

---

## Daily workflows

### "Extract IP addresses from a log"
```sh
perl -nE 'say $1 while /\b(\d{1,3}(?:\.\d{1,3}){3})\b/g' access.log | sort -u
```

### "Sum a column in a CSV"
```sh
perl -F, -ane '$sum += $F[2]; END { printf "%.2f\n", $sum }' data.csv
```

### "In-place rename extension"
```sh
perl -pi -e 's/\.txt$/.md/' *.txt
# Note: this changes file content, not filenames. For renaming:
rename 's/\.txt$/.md/' *.txt     # rename utility (may not be installed)
```

### "Extract unique lines from sorted input"
```sh
perl -ne 'print unless $seen{$_}++' file.txt
```

## Gotchas / Golden rules

1. **`use strict; use warnings;` — always** — without strict, Perl silently creates global variables on first use, leading to subtle bugs; without warnings, many mistakes go unreported.
2. **`@_` is the argument list in subs — always unpack it** — never modify `@_` directly (it aliases the caller's variables); copy at the start with `my @args = @_`.
3. **Context matters: `@arr` in scalar context is its length** — `my $n = @arr` gives the count, not the array.
4. **`chomp` removes the input record separator (`$/`), not just `\n`** — on Windows that's `\r\n`; best to set `$/` or use `s/\r?\n$//`.
5. **`die` without `or die` at `open` is the number one Perl bug** — every `open` call must have `or die "message: $!"` to surface failures.
