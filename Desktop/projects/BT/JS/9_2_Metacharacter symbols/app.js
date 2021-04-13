let re;
//Literal Characters
re = /hello/;
re = /hello/i;

// Metacharacter Symbols
re = /^h/i;         //Must start with
re = /world$/i;     // Must end with
re = /^hello$/i;    // Must begin and end with hello
re = /^h.llo$/i;    // Matches any ONE character
re = /^h*llo$/i;    // Matches any character 0 or more times
re = /gr?a?y/i;     //Optional character
re = /gr?a?y\?/i;   //Escape character
//Brackets [] - character Sets
re = /gr[ae]y/i;    //Must contain a or e
re = /[GF]ray/;     //Must be a G or F
re = /[^GF]ray/i;   //Match anything except a G or F
re = /[A-Z]ray/;    //Match any uppercase letter
re = /[a-z]ray/;    //Match any lowercase letter
re = /[A-Za-z]ray/; //Match any  letter
re = /[0-9]ray/     //Match any digit

// Braces {} - Quantifiers
re = /Hel{2}o/i;    // Must occur exactly {m} amount time
re = /Hel{2,4}o/i;    // Must occur exactly {m,n} m to n amount time
re = /Hel{2,}o/i;    // Must occur at least {m} times

// Parentheses () - Grouping
re = /([0-9]x){3}/  //Ex: 2x2x2x 3x3x3x 9x9x9x 7x7x7x

//Shoerhand Character Classes
re = /\w/;          //Word character - alphanumetic or _
re = /\w+/;         // + = one or more
re = /\W/;          // None-word character
re = /\d/;          // Match any digit
re = /\d+/;         // Match any digit 0 or more times
re = /\D/;          // Match any Non-digit
re = /\s/;          // Match whitespace char
re = /\S/;          // Match Non- whitespace char
re = /Hell\b/i;     // Word boundary

//Assertions
re = /x(?=y)/;      // Match x only if followed by y
re = /x(?!y)/;      // Match x only if NOT followed by y


// String to match
const str = 'Gray?';

//Log Results
const result = re.exec(str);
console.log(result);

function reTest(re, str) {
    if(re.test(str)){
        console.log(`${str} matches ${re.source}`);
    } else {
        console.log(`${str} does NOT match ${re.source}`);
    }
}

reTest(re, str);