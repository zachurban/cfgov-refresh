'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var mqr = require( 'gulp-mq-remove' );
var pkg = require( '../config' ).pkg;
var banner = require( '../config' ).banner;
var config = require( '../config' ).styles;
var glob = require( 'glob' );
var path = require( 'path' );
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

/**
 * Process modern CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesModern() {
  return gulp.src( config.cwd + config.src )
    .pipe( $.sourcemaps.init() )
    .pipe( $.less( config.settings ) )
    .on( 'error', handleErrors )
    .pipe( $.autoprefixer( {
      browsers: [ 'last 2 version',
                  'not ie <= 8',
                  'android 4',
                  'BlackBerry 7',
                  'BlackBerry 10' ]
    } ) )
    .pipe( $.header( banner, { pkg: pkg } ) )
    .pipe( $.sourcemaps.write( '.' ) )
    .pipe( gulp.dest( config.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process legacy CSS for IE7 and 8 only.
 * @returns {PassThrough} A source stream.
 */
function stylesIe() {
  return gulp.src( config.cwd + config.src )
    .pipe( $.less( config.settings ) )
    .on( 'error', handleErrors )
    .pipe( $.autoprefixer( {
      browsers: [ 'ie 7-8' ]
    } ) )
    .pipe( mqr( {
      width: '75em'
    } ) )
    // mqr expands the minified file
    .pipe( $.cssmin() )
    .pipe( $.rename( {
      suffix:  '.ie',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( config.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process stand-alone atomic component CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesOnDemand() {
  var files = glob.sync( config.cwd + '/on-demand/**/*.less' );
  var streams = files.map( function( file ) {
    var dirs = path.dirname( file ).split('/');
    var prefix = '.' + dirs[ dirs.length-1 ].charAt(0) + '-';
    var className = prefix + path.basename( file, '.less' );
    return gulp.src( file )
      .pipe( $.less( config.settings ) )
      .on( 'error', handleErrors )
      .pipe( $.autoprefixer( {
        browsers: [ 'last 2 version',
                    'ie 7-8',
                    'android 4',
                    'BlackBerry 7',
                    'BlackBerry 10' ]
      } ) )
      .pipe( $.header( banner, { pkg: pkg } ) )
      .pipe( $.wrapper( {
        header: className + ' {',
        footer: '}'
      } ) )
      .pipe( gulp.dest( config.dest ) )
      .pipe( browserSync.reload( {
        stream: true
      } ) );
  } );
}

gulp.task( 'styles:modern', stylesModern );
gulp.task( 'styles:ie', stylesIe );
gulp.task( 'styles:ondemand', stylesOnDemand );

gulp.task( 'styles', [
  'styles:modern',
  'styles:ie'
] );
