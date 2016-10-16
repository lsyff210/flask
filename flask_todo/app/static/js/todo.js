/**
 * Created by jinlinlin on 2016/6/24.
 */
    $(function(){

//{# 复选框操作，完成时，添加中间线，并且更改复选框对应编辑表单input-value为1，自动点击提交按钮；取消时相反       #}
        $("ol input[type='checkbox']").click(function(){
            var check_input = $(this).closest('.list-group-item').find('.check_input');
            if($(this).is(':checked')==true){
                alert('又完成一项工作，放松一下吧！');
                 check_input.attr('value','1');
                $(this).closest('.list-group-item').find('.p1').addClass('completed_item');
                $(this).closest('.list-group-item').find('.check_button').trigger('click');

            }else{
                alert('你确定要重新开始这个工作吗？');
                check_input.attr('value','2');
                $(this).closest('.list-group-item').find('.p1').removeClass('completed_item');
                $(this).closest('.list-group-item').find('.check_button').trigger('click');
            }
        });


//{#编辑按钮触发，显示需要输入的input   #}
        $('.edit').click(function(){
            var p = $(this).closest('.list-group-item').find('.p1');
            p.css('display', 'none');
            $(this).closest('.list-group-item').find('.in_form').css('display', 'block');
        });

//{#网页加载后，根据数据库state的数据，确定复选框操作        #}
         $(document).ready(function(){
            $("input[name='check_input']").each(function(){
                var val_check = $(this).val();
                var check = $(this).closest('.checkbox').find('.pull-right');
                if(val_check == 1){
                    check.attr('checked','checked');
                    $(this).closest('.list-group-item').find('.p1').addClass('completed_item');
                }
            })
         });

//{#正则验证        #}
//    {# 添加时的验证       #}
        $("input[name='add_list']").click(function(){
            var str = $(this).closest('.label_addlist').find('.form-control').val();
            var ret = /\S/;
            if(ret.test(str)==false){
                alert('您输入的内容为空，请重新输入');
                return false;
            };
        });
    });