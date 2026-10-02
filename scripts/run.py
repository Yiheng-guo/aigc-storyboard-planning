#!/usr/bin/env python3
"""Local structured-input helper. Semantic judgments must be supplied or reviewed by a human/agent."""
import argparse, json, sys, math
from pathlib import Path
from datetime import date

def need(condition, message):
    if not condition: raise ValueError(message)
def ids(rows, label):
    seen=set()
    for row in rows:
        value=row.get('id'); need(isinstance(value,str) and value.strip(),label+' requires nonempty id')
        need(value not in seen,label+' duplicate id: '+value);seen.add(value)
    return seen
def number(value, label):
    need(not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value),label+' must be finite number');return value

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        need(not args.output.exists(),'refusing to overwrite output')
        data=json.loads(args.input.read_text(encoding='utf-8'));need(isinstance(data,dict),'input must be object')
        result=process(data)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
        print(json.dumps({'output':str(args.output),'status':result.get('status','completed')},ensure_ascii=False))
        return 0 if result.get('status') not in ('blocked','failed') else 2
    except (ValueError,KeyError,TypeError,OSError) as e: print('error: '+str(e),file=sys.stderr);return 2

def process(d):
    need(d.get('script_confirmed') is True,'script must be confirmed');shots=d['shots'];need(shots,'shots required');ids(shots,'shots')
    findings=[];previous=None;total=0
    for shot in shots:
        number(shot['duration_seconds'],'duration');need(shot['duration_seconds']>0,'positive duration required');total+=shot['duration_seconds']
        for field in ('scene_id','character_ids','action','dialogue','camera','start_state','end_state','reference_assets','generation_prompt'): need(field in shot,'missing '+field)
        need(shot['action'] and shot['camera'] and shot['generation_prompt'],'action/camera/prompt required')
        need(isinstance(shot['start_state'],dict) and isinstance(shot['end_state'],dict),'states must be objects')
        if previous and previous['scene_id']==shot['scene_id']:
            a,b=previous['end_state'],shot['start_state'];transitions=shot.get('explicit_transitions',{})
            for key in set(a)|set(b):
                if a.get(key)!=b.get(key) and not transitions.get(key): findings.append({'from':previous['id'],'to':shot['id'],'state':key,'previous':a.get(key),'current':b.get(key),'issue':'unexplained state discontinuity'})
        previous=shot
    target=number(d['target_seconds'],'target_seconds')
    if abs(total-target)>1/24: findings.append({'issue':'total duration mismatch','planned':total,'target':target})
    return {'status':'blocked' if findings else 'ready_for_visual_review','duration_seconds':total,'findings':findings,'shots':shots,'limits':'State checking does not verify face identity, lip sync or rendered images.'}

if __name__ == "__main__": raise SystemExit(main())
