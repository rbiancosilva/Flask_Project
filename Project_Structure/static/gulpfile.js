const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const sourcemaps = require('gulp-sourcemaps');
const uglify = require('gulp-uglify');

function comp_sass(){
    return gulp.src('./src/styles/*scss') // Sets source folder for scss files
        .pipe(sourcemaps.init()) //Used to source the production style map to the scss file instead of the css production one
        .pipe(sass({outputStyle:'compressed'})) //Compresses CSS output file
        .pipe(sourcemaps.write('./maps')) //Sets destination for css.map files
        .pipe(gulp.dest('build/styles')); //Sets destination for SCSS files compiled  to CSS
}

function comp_js () {
    return gulp.src('./src/scripts/*js') // Sets source folder for pre-compilation JS files
        .pipe(uglify()) //Compresses JS files
        .pipe(gulp.dest('build/scripts')); //Sets destination for compressed JS files
}

exports.default = function () {
    gulp.watch('./src/styles/*scss', {ignoreInitial:false}, gulp.series(comp_sass));
    gulp.watch('./src/scripts/*js', {ignoreInitial:false}, gulp.series(comp_js));
    
}