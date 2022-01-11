test_iterations=2
thread_nums=(3 4 5 6 7 8 9 10 11 12)
problem_sizes=(500 1500 3000)

report_file_1='measurements/task1.csv'
report_file_2='measurements/task2.csv'
report_file_3='measurements/task3.csv'

echo "thread_num;problem_size;time" > $report_file_1
echo "thread_num;problem_size;time" > $report_file_2
echo "thread_num;problem_size;time" > $report_file_3
for i in $(seq 1 $test_iterations); do
    for problem_size in "${problem_sizes[@]}"; do
        command="python3 ./task_0.py $problem_size"
        echo $command
        time=$($command)
        printf "1;%d;%lf\n" $problem_size $time >> $report_file_1
        printf "1;%d;%lf\n" $problem_size $time >> $report_file_2
        printf "1;%d;%lf\n" $problem_size $time >> $report_file_3
        for thread_num in "${thread_nums[@]}"; do
            command="mpiexec -n $thread_num python3 ./task_1.py $problem_size"
            echo $command
            time=$($command)
            printf "%d;%d;%lf\n" $thread_num $problem_size $time >> $report_file_1

            command="mpiexec -n $thread_num python3 ./task_2.py $problem_size"
            echo $command
            time=$($command)
            printf "%d;%d;%lf\n" $thread_num $problem_size $time >> $report_file_2

            command="mpiexec -n $thread_num python3 ./task_3.py $problem_size"
            echo $command
            time=$($command)
            printf "%d;%d;%lf\n" $thread_num $problem_size $time >> $report_file_3
        done
    done
done