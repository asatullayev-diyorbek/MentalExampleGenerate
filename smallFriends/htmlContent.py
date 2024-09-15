import asyncio

from .smallFriend import small_friend
from .logo_base64 import base64_logo


def html_content(column, digits, count, mode, requirement, method):

    style_css = """
        <style>
            @page{margin:10px}table{page-break-inside: avoid;width:100%;border-collapse:collapse;margin:20px 0;font-size:18px;font-family:Arial,
            sans-serif;text-align:center}thead tr{background-color:rgba(84,133,122,.62);color:#fff;text-align:center;font-weight:
            bold;border:1px solid #000}th,td{height:25px;border:1px solid #000}tbody tr:hover{background-color:#f1f1f1;cursor:
            pointer}th{width:10%;font-size:25px;font-weight:300;color:#000}.header{padding:10px 30px;display:flex;justify-content:
            end;align-items:center;text-align:center}.header span{font-size:20px;text-align:center}.header span i{font-size:20px;
            text-align:center} .results{height:45px} .new-page{page-break-before: always; page-break-inside: avoid;} .pdf-logo{width:50px;}
        </style>"""

    head_html = f"""
        <head>
            <meta charset="UTF-8">
            <title>Yulduzcha</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" integrity="
            sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg==" crossorigin=
            "anonymous" referrerpolicy="no-referrer" />
            {style_css}
        </head>
    """

    header_block = f"""
        <div class="header">
            <span class="logo">
                 <img class='pdf-logo' src="{base64_logo}" alt="logo"> Yulduzcha<br>
                <i> Generatsiyasi</i>
            </span>
        </div>
    """

    title_block = f"""
        <h3 class="title">
            {column} ustun {mode} {digits} xona {requirement} {count * 10} ta {'parallel' if method == 'parallel' else 'aralash'}
        </h3>
    """

    example_tables = []
    result_tables = []

    for i in range(count):
        res = small_friend(column=column, digits=digits, count=10, requirement=requirement, method=method)

        thead_piece = f"""
            <thead>
                <tr>
                    {''.join(f'<th>{i * 10 + j + 1}</th>' for j in range(len(res['examples'])))}
                </tr>
            </thead>
        """

        def td_piece(n, data):
            return ''.join(f"<td>{row[n]}</td>" for row in data)

        tbody_piece = f"""
            <tbody>
                {''.join(f"<tr>{td_piece(j, res['examples'])}</tr>" for j in range(len(res['examples'][0])))}
                <tr>{''.join("<td> </td>" for _ in range(len(res['examples'])))}</tr>
                <tr>{''.join("<td> </td>" for _ in range(len(res['examples'])))}</tr>
            </tbody>
        """

        tbody_piece_result = f"""
            <tbody>
                <tr>
                    {''.join(f"<td>{j}</td>" for j in res['results'])}
                </tr>
            </tbody>
            """

        example_table = f"""
            <table>
                {thead_piece}
                {tbody_piece}
            </table>
        """

        result_table = f"""
            <table class='results'>
                {thead_piece}
                {tbody_piece_result}
            </table>
        """

        example_tables.append(
            example_table
        )

        result_tables.append(
            result_table
        )
    content = "<html lang='eng'>\n"
    content += head_html + '\n'
    content += "<body>"
    content += header_block + '\n'
    content += title_block + '\n'
    for et in example_tables:
        content += et + '\n'
    content += "<br><br><br>"
    content += "<div class=new-page>" + '\n'
    content += "<h3>&nbsp;&nbsp;&nbsp;&nbsp;Javoblar:</h3>" + '\n'
    for rt in result_tables:
        content += rt + '\n'
    content += "</div>"
    content += "</body>\n</html>"
    return content

