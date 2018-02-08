import os
import getopt
import sys
import pdb

def getResultFromLog(filename):
    """Capture last table of output, sort the nodes in the distance vector alphabetically,
    and output the sorted table as a string."""
    with open(filename) as f:
       s = f.read()
    last_table = s.split('-----\n') # The last element in list will be '', and second-last element is the final dv table
    result = ''
    for line in last_table[-2].strip().split('\n'):
        k,dv = line.split(':')
        nodes_weights = dv.split(',')
        result += k + ':' + ','.join(sorted(nodes_weights)) + '\n'
    return result

def main(argv):
    student_file = ' '
    ref_file = ' '
    try:
        opts, args = getopt.getopt(argv,"s:r:",["student_file=","ref_file="])
    except getopt.GetoptError:
        print 'compare_logs.py -s <student_file> -r <ref_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--student_file"):
           student_file = arg
        elif opt in ("-r", "--ref_file"):
           ref_file = arg

    # Sort nodes in distance vectors
    ref_result = getResultFromLog(ref_file)
    student_result = getResultFromLog(student_file)

    # Output
    student_lines = student_result.strip().split('\n')
    ref_lines = ref_result.strip().split('\n')
    for n in range(max(len(student_lines), len(ref_lines))):
        if len(student_lines) < n+1:
            print 'STU: Missing line <==============='
            print 'REF: %s' % ref_lines[n]
            print '-'
        elif len(ref_lines) < n+1:
            print 'STU: %s <===============' % student_lines[n]
            print 'REF: Missing line'
            print '-'
        elif student_lines[n] != ref_lines[n]:
            print 'STU: %s <===============' % student_lines[n]
            print 'REF: %s' % ref_lines[n]
            print '-'
        else:
            print 'STU: %s' % student_lines[n]
            print 'REF: %s' % ref_lines[n]
            print '-'
            
    if ref_result == student_result:
        print "Perfect match"
    else:
        print 'Differences found'

if __name__ == "__main__":
   main(sys.argv[1:])

