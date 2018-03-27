const envvars = require( '../../config/environment' ).envvars;
const fancyLog = require( 'fancy-log' );
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const isReachable = require( 'is-reachable' );
const localtunnel = require( 'localtunnel' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const psi = require( 'psi' );

// An example of running Pa11y on multiple URLS
'use strict';

const pa11y = require( 'pa11y' );

// Async function required for us to use await
async function runExample() {
  try {

    // Put together some options to use in each test
    const options = {
      log: {
        debug: console.log,
        error: console.error,
        info: console.log
      },
      standard: 'WCAG2AA'
    };

    // Run tests against multiple URLs
    const results = await Promise.all([
      pa11y('http://localhost:8000/', options),
      pa11y('http://localhost:8000/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/', options)
    ]);

    // Output the raw result objects
    console.log(results[0]); // Results for the first URL
    console.log(results[1]); // Results for the second URL

  } catch (error) {

    // Output an error if it occurred
    console.error(error.message);

  }
}


gulp.task( 'pa11y', runExample );
