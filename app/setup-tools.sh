
#----------
# Setup DSSP : 

./tools/DSSP/DsspCompileCC

path_dssp=`realpath tools/DSSP/dsspcmbi`
replacement='my $path_dssp="'$path_dssp'";'
sed -i "38s/.*/${replacement//\//\\/}/"  tools/DSSPPII/dssppII.pl


#---------
# Setut PROSS

# Nothing to do
