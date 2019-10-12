const sass = require('node-sass');


module.exports = function (grunt) {
    require('load-grunt-tasks')(grunt);
    grunt.initConfig({
        concat: {
            js: {
                src: ['assets/js/**/*.js'],
                dest: 'build/html/static/dist/js/scripts.js',
            }

        },
        uglify: {
            my_target: {
                files: {
                    'build/html/static/dist/js/scripts.js': ['build/html/static/dist/js/scripts.js']
                }
            }
        },
        sass: {
            options: {
                implementation: sass,
                sourceMap: true
            },
            dist: {
                files: {
                    'build/html/static/dist/css/app.css': 'assets/scss/main.scss'
                }
            }
        },
        cssmin: {
            options: {
                shorthandCompacting: false,
                roundingPrecision: -1
            },
            target: {
                files: {
                    'build/html/static/dist/css/app.css': ['build/html/static/dist/css/app.css']
                }
            }
        },
        watch: {
            js: {
                files: 'assets/js/**/*.js',
                tasks: ['concat:js', 'uglify'],
            },
            sass: {
                files: 'assets/scss/**/*.scss',
                tasks: ['sass', 'cssmin']
            }

        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin', 'watch']);
    grunt.registerTask('build', ['concat', 'uglify', 'sass', 'cssmin']);
};