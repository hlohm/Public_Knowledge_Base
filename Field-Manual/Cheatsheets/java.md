---
type: cheatsheet
area: "Programming Languages"
aliases: [Java, JVM]
tags: [java, programming, oop, jvm, maven, gradle]
status: working
---

# Java

> **Area:** [[Programming Languages]]

Java 17 LTS — the features and idioms in everyday use. Build tooling with Maven and Gradle. Assumes you know the syntax; this is a reminder and a gotcha list.

---

## 1. Types and declarations

```java
// Primitives vs wrappers
int    n = 42;      Integer N = 42;       // autoboxed
long   l = 42L;     Long    L = 42L;
double d = 3.14;    Double  D = 3.14;
boolean b = true;   Boolean B = true;
char   c = 'A';     Character C = 'A';

// Type inference (Java 10+)
var items = new ArrayList<String>();
var entry = map.entrySet().iterator().next();

// String (immutable; use StringBuilder for concatenation in loops)
String s = "hello";
s.length(), s.charAt(0), s.substring(1, 4)
s.toUpperCase(), s.toLowerCase(), s.trim(), s.strip()   // strip() is Unicode-aware
s.contains("ell"), s.startsWith("he"), s.endsWith("lo")
s.replace("l", "r"), s.replaceAll("\\d+", "N")        // replaceAll uses regex
s.split(","), String.join(",", list)
s.formatted("Hello %s", name)     // Java 15+ alias for String.format
String.valueOf(42)                 // int → String
Integer.parseInt("42")            // String → int (throws NumberFormatException)
s.isBlank()                       // true if empty or only whitespace (Java 11+)

// Text blocks (Java 15+)
String json = """
        {
          "name": "Alice",
          "age": 30
        }
        """;    // leading whitespace stripped based on closing delimiter
```

## 2. Collections

```java
import java.util.*;

// List
List<String> list = new ArrayList<>();
list.add("a"); list.add("b");
list.get(0);              // "a"
list.set(0, "A");         // replace
list.remove(0);           // by index
list.remove("b");         // by value (first occurrence)
list.size();
Collections.sort(list);
Collections.unmodifiableList(list);

// Immutable factory (Java 9+)
List<String> immutable = List.of("a", "b", "c");
Map<String, Integer> immutableMap = Map.of("a", 1, "b", 2);
Set<String> immutableSet = Set.of("x", "y");

// Map
Map<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.get("a");                        // 1 (null if missing)
map.getOrDefault("z", 0);           // 0
map.containsKey("a");
map.putIfAbsent("b", 2);
map.computeIfAbsent("list", k -> new ArrayList<>()).add("value");
for (Map.Entry<String, Integer> e : map.entrySet()) {
    System.out.println(e.getKey() + " = " + e.getValue());
}

// Set
Set<String> set = new HashSet<>();
set.add("x"); set.remove("x"); set.contains("x");

// Queue / Deque
Deque<String> deque = new ArrayDeque<>();
deque.addFirst("front");
deque.addLast("back");
deque.pollFirst();     // removes and returns (null if empty)
deque.peekFirst();     // returns without removing
```

## 3. Streams (Java 8+)

```java
import java.util.stream.*;

List<String> names = List.of("Alice", "Bob", "Charlie");

// Common pipeline
List<String> result = names.stream()
    .filter(n -> n.length() > 3)
    .map(String::toUpperCase)
    .sorted()
    .collect(Collectors.toList());

// toList() — Java 16+ (unmodifiable)
List<String> result = names.stream()
    .filter(n -> n.length() > 3)
    .toList();

// Count / find
long count = names.stream().filter(n -> n.startsWith("A")).count();
Optional<String> first = names.stream().filter(n -> n.startsWith("A")).findFirst();
boolean anyMatch  = names.stream().anyMatch(n -> n.startsWith("A"));
boolean allMatch  = names.stream().allMatch(n -> n.length() > 2);

// Reduce
int sum = IntStream.rangeClosed(1, 10).sum();
int total = numbers.stream().mapToInt(Integer::intValue).sum();
Optional<Integer> max = numbers.stream().max(Comparator.naturalOrder());

// Grouping and partitioning
Map<Integer, List<String>> byLength = names.stream()
    .collect(Collectors.groupingBy(String::length));

Map<Boolean, List<String>> partitioned = names.stream()
    .collect(Collectors.partitioningBy(n -> n.length() > 3));

// String joining
String joined = names.stream().collect(Collectors.joining(", ", "[", "]"));

// flatMap
List<String> words = sentences.stream()
    .flatMap(s -> Arrays.stream(s.split(" ")))
    .collect(Collectors.toList());
```

## 4. Optional (Java 8+)

```java
Optional<String> opt = Optional.ofNullable(possiblyNull);

opt.isPresent()                // explicit check (verbose)
opt.isEmpty()                  // Java 11+
opt.get()                      // throws NoSuchElementException if empty
opt.orElse("default")          // value or default
opt.orElseGet(() -> compute())  // lazy default
opt.orElseThrow()              // throw NoSuchElementException
opt.map(String::toUpperCase)   // transform if present
opt.filter(s -> s.length() > 3)
opt.ifPresent(System.out::println)
opt.ifPresentOrElse(
    v -> use(v),
    () -> handleAbsent()
);
```

## 5. Exceptions

```java
// Checked vs unchecked
// - RuntimeException subclasses: unchecked, don't need to be declared/caught
// - Exception subclasses (not Runtime): checked, must catch or declare throws

// Try-with-resources (auto-closes Closeable / AutoCloseable)
try (BufferedReader br = new BufferedReader(new FileReader("f.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        process(line);
    }
} catch (IOException e) {
    System.err.println("Error: " + e.getMessage());
}

// Multi-catch
try {
    ...
} catch (NumberFormatException | IllegalArgumentException e) {
    log(e);
}

// Re-throw with cause
} catch (Exception e) {
    throw new RuntimeException("Context: " + e.getMessage(), e);
}

// Custom exception
public class ServiceException extends RuntimeException {
    private final int code;
    public ServiceException(String message, int code) {
        super(message);
        this.code = code;
    }
    public int getCode() { return code; }
}
```

## 6. Records (Java 16+)

```java
// Records are immutable data carriers — auto-generate constructor, accessors, equals, hashCode, toString
public record Point(double x, double y) {}

Point p = new Point(1.0, 2.0);
p.x()   // accessor (not getX())
p.y()

// Compact constructor (validation)
public record Range(int start, int end) {
    Range {
        if (end < start) throw new IllegalArgumentException("end < start");
    }
}

// Records can implement interfaces
public record Name(String first, String last) implements Comparable<Name> {
    @Override public int compareTo(Name o) {
        return this.last.compareTo(o.last);
    }
}
```

## 7. Maven

```sh
# Compile
mvn compile

# Run tests
mvn test
mvn test -Dtest=MyClassTest              # specific test class
mvn test -Dtest=MyClassTest#myMethod     # specific test method

# Package (creates JAR in target/)
mvn package
mvn package -DskipTests                  # skip tests for speed

# Install to local repo (~/.m2)
mvn install

# Clean
mvn clean
mvn clean package                        # rebuild from scratch

# Run (if main class defined in pom.xml)
mvn exec:java -Dexec.mainClass="com.example.Main"

# Add dependency
# Add to pom.xml <dependencies>:
# <dependency>
#     <groupId>com.google.guava</groupId>
#     <artifactId>guava</artifactId>
#     <version>33.0.0-jre</version>
# </dependency>

# Show dependency tree
mvn dependency:tree
```

## 8. Gradle

```sh
# Compile
./gradlew compileJava

# Run tests
./gradlew test
./gradlew test --tests "com.example.MyClassTest"

# Build JAR
./gradlew build
./gradlew build -x test

# Run
./gradlew run

# Show dependencies
./gradlew dependencies

# Add dependency in build.gradle(.kts):
# dependencies {
#     implementation("com.google.guava:guava:33.0.0-jre")
#     testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
# }
```

---

## Files & locations

| Path | Purpose |
|---|---|
| `pom.xml` | Maven build configuration (dependencies, plugins) |
| `build.gradle` / `build.gradle.kts` | Gradle build config |
| `src/main/java/` | Production source root |
| `src/test/java/` | Test source root |
| `src/main/resources/` | Non-Java resources (configs, templates) |
| `~/.m2/repository/` | Local Maven cache |

## Gotchas / Golden rules

1. **`==` compares references for objects** — always use `.equals()` to compare `String`, `Integer`, and other objects; `==` compares reference identity.
2. **`Integer` caching: `-128` to `127`** — small `Integer` values from autoboxing may be the same object (`== true`); outside that range they are not. This makes `==` on `Integer` unreliable.
3. **`HashMap` does not guarantee order** — use `LinkedHashMap` for insertion-order or `TreeMap` for sorted order.
4. **Streams are lazy until a terminal operation** — calling `.filter().map()` alone does nothing; you need a terminal (`.collect()`, `.forEach()`, `.count()`) for anything to execute.
5. **Checked exceptions cannot propagate through lambdas/streams** — wrap them in a `RuntimeException` or use a functional interface that declares the checked exception.
