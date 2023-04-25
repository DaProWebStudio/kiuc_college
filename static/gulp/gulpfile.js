const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const cleanCSS = require('gulp-clean-css');
const autoprefixer = require('gulp-autoprefixer');
const rename = require("gulp-rename");

gulp.task('watch', function () {
    gulp.watch("../sass/**/*.+(scss|sass|css)", gulp.parallel('styles'));
});
gulp.task('styles', function () {
    return gulp.src("../sass/**/*.+(scss|sass)")
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(rename({suffix: '.min', prefix: ''}))
        .pipe(autoprefixer())
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(gulp.dest("../css/"));
});

gulp.task('default', gulp.parallel('watch', 'styles'));