from board.models import Board
from member.models import Member

from django.shortcuts import render, redirect
from django.db.models import F
from django.views.decorators.cache import cache_control

# Create your views here.

# 데코레이터로 웹페이지의 캐시기능을 중지함
@cache_control(no_cahe=True, no_store=True, must_revalidate=True)
def list(request):
    # select 'id','title','userid','regdate','views'
    # from board order by id desc
    # bdlist = board.objects.values('id','title','userid','regdate','views').order_by('-id')

    # board와 Member 테이블은 userid <-> id 컬럼을 기준으로
    # inner join 을 수행
    bdlist = Board.objects.select_related('member')

    # join된 member 테이블의 userid 확인
    # bdlist.get(0).member.userid

    context = {'bds': bdlist}
    return render(request, 'board/list.html', context)

#게시판 본문보기 처리
def view(request):
    if request.method == 'GET':
        form = request.GET.dict()
        # print(form['bno'])

        # 본문글에 대한 조회수 증가
        # upadte board set views = views + 1
        # where id = ???

        # b = Board.objects.get(id=form['bno'])
        # b.views = b.views + 1
        # b.save()

        Board.objects.filter(id=form['bno']).update(views=F('views') + 1)

        # 본문글 조회
        # select * from board inner join member
        # using(id) where id = ???
        bd = Board.objects.select_related('member').get(id=form['bno'])

    elif request.method == 'POST':
        pass

    context = {'bd': bd}
    return render(request, 'board/view.html',context)

# get : boart/write.html로 이동
# post : 작성한 글을 DB에 저장, 'board/list.html로 이동
def write(request):
    returnPage = 'board/write.html'
    form = ''
    error = ''
    if (request.method == 'GET'):
        pass
    elif (request.method == 'POST'):
        form = request.POST.dict()

        # 유효성 검사 1

        if not (form['title'] and form['contents']):
            error = '제목이나 본문을 작성하세요!'
        else:
            # 입력한 게시글을 board객체에 담음
            bd = Board( title=form['title'],
                        contents=form['contents'],
                        # 새글을 작성한 회원에 대한 정보는
                        # 회원테이블에 존재하는 회원번호를 조회해서
                        # userid 속성에 저장
                        member=Member.objects.get(pk=form['memberid']) )
            bd.save()   # board객체에 당은 게시글을 테이블에 저장

            return  redirect('/list')

    context = { 'form': form, 'error': error}
    return render(request, returnPage, context)

# 분문글 삭제하기
# /remove?bno=***
def remove(request):
    if request.method == 'GET':
        form =request.GET.dict()

        # delete from board where bno = ??
        Board.objects.filter(id=form['bno']).delete()
    return redirect('/list')

# 분문글 수정하기
def modify(request):
    bd = None
    if request.method == 'GET':
        form = request.GET.dict()
        # update board set title = ???, contents = ???
        # where

        # select * from board where bno = ???
        bd = Board.objects.get(id=form['bno'])

    elif request.method =='POST':
        form = request.POST.dict()
        # update board set title = ???, contents = ???
        # where bno = ???
        # b = Board.objects.get(id=form['bno'])
        # b.title = form['title']
        # b.contents = form['contents']
        # b.save()

        Board.objects.filter(id=form['bno']).update(title=form['title'], contents=form['contents'])

        # 본문글 수정완료시 view 페이지로 이동
        return redirect('/view?bno=' + form['bno'])

    context = {'bd': bd}
    return render(request, 'board/modify.html', context)