from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

semantic_cls = pipeline(Tasks.information_extraction, 'asset/model')
semantic_cls(input='高捷，祖籍江苏，本科毕业于东南大学')
