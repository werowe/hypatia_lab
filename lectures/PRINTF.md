# `printf()` in C

`printf()` displays text and variable values.

```c
printf("format", value);
```

## Common Format Specifiers

| Specifier | Data type | Example |
|---|---|---|
| `%d` or `%i` | `int` | `printf("%d", age);` |
| `%u` | `unsigned int` | `printf("%u", number);` |
| `%ld` | `long int` | `printf("%ld", population);` |
| `%lld` | `long long int` | `printf("%lld", bigNumber);` |
| `%f` | `float` or `double` | `printf("%f", temperature);` |
| `%e` | Scientific notation | `printf("%e", number);` |
| `%c` | One character | `printf("%c", letter);` |
| `%s` | String or character array | `printf("%s", name);` |
| `%x` | Hexadecimal | `printf("%x", number);` |
| `%o` | Octal | `printf("%o", number);` |
| `%p` | Memory address or pointer | `printf("%p", (void *)&number);` |
| `%%` | Percent sign | `printf("50%%");` |

## Decimal Places

```c
printf("%.2f", price);        // 12.35
printf("%.1f", temperature);  // 22.5
```

## Width and Alignment

```c
printf("%5d", number);    // Minimum width of 5, aligned right
printf("%-5d", number);   // Minimum width of 5, aligned left
printf("%05d", number);   // Fill unused positions with zeros
```

## Complete Example

```c
#include <stdio.h>

int main(void) {
    int age = 16;
    double height = 1.75;
    char grade = 'A';
    char name[] = "Anna";

    printf("Name: %s\n", name);
    printf("Age: %d\n", age);
    printf("Height: %.2f metres\n", height);
    printf("Grade: %c\n", grade);

    return 0;
}
```

## Starting a New Line

Use `\n` to start a new line:

```c
printf("First line\n");
printf("Second line\n");
```

## Printing Multiple Values

Multiple values can appear in one `printf()` statement:

```c
printf("%s is %d years old.\n", name, age);
```
