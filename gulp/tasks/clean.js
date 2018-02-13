const configClean = require( '../config' ).clean;
const del = require( 'del' );
const gulp = require( 'gulp' );

gulp.task( 'clean:css', done => {
  // Clean CSS out of /cfgov/static_built/css/
  del( configClean.css + '/**/*' );
  done();
} );

gulp.task( 'clean:js', done => {
  // Clean JavaScript out of /cfgov/static_built/js/
  del( configClean.js + '/**/*' );
  done();
} );

gulp.task( 'clean', done => {
  // Clean everything out of /cfgov/static_built/
  del( configClean.dest + '/**/*' );
  done();
} );
