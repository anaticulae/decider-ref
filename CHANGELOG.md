# changelog

Every noteable change is logged here.

## v1.9.1

## v1.9.0

### Feature

* add description links to linter message (925d6576ab80)
* make message more user friendly (24162caa90cc)
* use improve inside approach (4814b9b25fde)
* add typo error detector (014dba8f55e4)
* verify opening and closing brackets (5a21470a1f57)
* disable bib ref check if bib is not parsed properly (439d2d9c28ca)
* use nltk stopwords (98cdb7169389)
* disable balance check for very short sections (a50a7db13f73)
* show bib on detected page (f9383901b33d)
* show bib linter warning to bib page (bf0bfb1fbd17)
* add location to detected abbr table message (e83167d5c800)
* use improved legal checker (4eb75931f89f)
* add hint to simplify bib label (7fe999a42246)

### Fix

* handle roman numbers later (440af2291f57)
* clarify linter message (64f27ae1d2fb)
* skip disabled check (579621035c5b)
* clarify error message (652e479d2f9f)
* adjust newlines (b1ad28f95458)
* fix newlines (821c3e7a3943)
* adjust newlines (d9f3e998c311)

## v1.8.1

## v1.8.0

### Feature

* disable plot on to few bib items (48760e2a4863)
* add linter step to detect not required abbreviation (decbeae591b3)

### Fix

* skip invalid bib inside check (3db33d6979a3)
* do not fail on invalid bib reference (58af1828db99)

## v1.7.1

### Fix

* add protocol show list to decider_abbreviation (fc69c49bfa38)

## v1.7.0

### Feature

* add decider_abbreviation to judge different tables (0016d5453f52)

## v1.6.0

### Feature

* add protocol show list (e3aeb8d04b28)

## v1.5.1

### Feature

* add valid bib year range (be52b394576b)

### Fix

* do not fail on empty bib (5219e3374de9)
* do not mix Roman and Arabic numbers (a673823d53bd)

## v1.5.0

### Feature

* check more than level one (36d94625f67d)
* add location to toc finding (03fcd55fbbe4)
* select best headlines (5b196b00fb8e)

## v1.4.1

## v1.4.0

### Feature

* add bib year histogram plotter (ae9750c83496)

## v1.3.0

### Feature

* add missing bib table log (3a2480dfbd33)

### Fix

* fix theissen sort order (8eda9b308933)
* skip None reference for bib check (a8700f424147)
* do not inform user about not parse able reference (91c2b0411833)

### Documentation

* Happy New Year! (a5c85d7f9e5b)

## v1.2.2

### Fix

* add missing import (53c6d57a963e)

## v1.2.1

## v1.2.0

### Feature

* move decider toc from decider project (9763c3512152)

## v1.1.0

### Feature

* add step to verify that bib source is not used (80f818ae5e7d)
* verify that bib label exists in bib table (befcab56a56d)
* improve bib page check (35d66f8d1cd3)
* add label step to verify bib refs (4b8ee68d85fb)
* add parsed text bib refs as step input (bded4fb63d54)

## v1.0.0

### Feature

* rename repository name (c721b2aaa061)
* enable using decider_bibliography as cli (b9f2054d2387)
* shorten project name (bea93f770db1)
* ease importing path module (409df76121b5)

## v0.1.0

### Feature

* move bib-decider from decider project (9350d97050e5)
* add cli and test infrastructure (051e319110db)

### Fix

* adjust setup path (888493955616)

## v0.0.0 Initial release

