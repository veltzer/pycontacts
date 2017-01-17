############
# includes #
############
include /usr/share/templar/make/Makefile

##############
# parameters #
##############
# do you want to debug the makefile?
DO_MKDBG?=0

########
# code #
########
ifeq ($(DO_MKDBG),1)
Q=
# we are not silent in this branch
else # DO_MKDBG
Q=@
#.SILENT:
endif # DO_MKDBG

# this line guarantees that if a recipe fails then the target file
# will be deleted.
.DELETE_ON_ERROR:

###########
# targets #
###########
# do not touch this rule
all: $(ALL) $(ALL_DEP)
