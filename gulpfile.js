var gulp = require('gulp');
var sass = require('gulp-sass');
var ugly = require('gulp-uglify');

gulp.task('js',function () {
	gulp.src('assets/js/**/*.js')
	.on('error', function (error) { console.log(error) })
	.pipe(ugly())
	.on('error', function (error) { console.log(error) })
	.pipe(gulp.dest('static/js'))
	.on('error', function (error) { console.log(error) });
});

gulp.task('sass',function () {
	gulp.src('assets/sass/**/*.scss')
	.on('error', function (error) { console.log(error) })
	.pipe(sass())
	.on('error', function (error) { console.log(error) })
	.pipe(gulp.dest('static/css'))
	.on('error', function (error) { console.log(error) });
});

gulp.task('default', function () {
	gulp.watch('assets/js/*.js',['js']);
	gulp.watch('assets/sass/*.scss',['sass']);
});