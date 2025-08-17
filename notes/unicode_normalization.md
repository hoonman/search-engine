# Unicode Normalization
## Two main types of equivalence
* main idea: different unicode sequences can mean the same thing but have different binary representations.
* there are two formal types of equivalence between characters: (1) canonical equivalence and (2) compatibility equivalence

**canonical:** fundamental equivalency between characters or sequences of characters which represent the same abstract character and which when correctly displayed should always have the same visual appearance and behavior
* these are equivalence that SHOULD be the same after normalization.
* same characters stored differently.
* e.g. U+00E9 vs. U+0065 U+0301

**compatibility:** mean roughly the same thing but might differ in appearance, formatting, or usage.
* i^9 vs. i9
    * visually suggests the same thing but they are not canonically equivalent
    * normalize to different results under NFC / NFD
    * normalize to same results under NFKC / NFKD


## Four normalization forms 
1. **NFD:** Canonical Decomposition. decompose characters into their canonical components 
    * example:  
2. **NFC:** Canonical Decomposition + Composition. decompose, reorder combining marks, then recompose where possible to canonical composites. 
3. **NFKD:** Compatibility Decomposition -- decompose using compatibility mappings (breaks many formatting / compatbility characters)
4. **NFKC:** Compatibility Decomposition + Composition -- compatibility decomposition then canonical recomposition (so compatibility distinctions can be lost).


## Some important categorical terms
* singletons: 
* composites: single unicode code point that represents what could also be written as a base character + one or more combining marks
    * ex. é can be represented as (U+00E9)
    * if we break that char down, it combines the base (e -- U+0065) with (accent -- U+0301)
    * since composite means multiple this makes sense.
* canonical composites: if we decompose a composite and compose again but nothing changed, it is considered canonical composite
    * ex. decompose é -> e + accent -> recompose -> é again with same unicode code point = canonical composite !

 