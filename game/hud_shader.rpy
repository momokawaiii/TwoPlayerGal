init python:

    HUD_FUNCTIONS = """
        float iTime;
        
        #define PI 3.14159265359

        mat2 Rot(float a) { float c=cos(a); float s=sin(a); return mat2(c,-s,s,c); }
        float antialiasing(float n, vec2 res) { return n/min(res.y,res.x); }
        float S(float d, float b, vec2 res) { float aa=antialiasing(1.5,res); return smoothstep(aa,-aa,d-b); }
        float B(vec2 p, vec2 s) { vec2 d=abs(p)-s; return max(d.x,d.y); }
        vec2 R45(vec2 p) { return (p+vec2(p.y,-p.x))*0.707; }
        float Tri(vec2 p, vec2 s) { return max(R45(p).x,max(R45(p).y,B(p,s))); }
        vec2 DF(vec2 a, float b) { float ang=atan(a.y,a.x); float len=length(a); float seg=6.28/(b*8.); float mod_ang=mod(ang+seg,6.28/((b*8.)*0.5)); return len*cos(mod_ang+(b-1.)*seg+vec2(0.,11.)); }
        vec2 PUV(vec2 p) { return vec2(log(length(p)),atan(p.y,p.x)); }
        float checkChar(int target, int val) { return 1.-abs(sign(float(target)-float(val))); }

        float numMask(vec2 p){ vec2 pp=p; float d=B(p,vec2(0.35,0.35)); p.y=abs(p.y)-0.36; float a=radians(-45.); float d2=B(p,vec2(0.1,0.03)); p.x=abs(p.x)-0.08; d2=max(dot(p,vec2(cos(a),sin(a))),d2); d=max(-d2,d); p=pp; p.x=abs(p.x)-0.36; a=radians(-45.); d2=B(p,vec2(0.03,0.1)); p.y=abs(p.y)-0.08; d2=max(-dot(p,vec2(cos(a),sin(a))),d2); d=max(-d2,d); p=pp; a=radians(50.); p=abs(p)-0.32; d=max(dot(p,vec2(cos(a),sin(a))),d); return d; }
        float num0(vec2 p){ vec2 pp=p; float d=B(p-vec2(-0.05,0.29),vec2(0.12,0.06)); p*=Rot(radians(-45.)); p-=vec2(-0.01,0.33); float d2=B(p,vec2(0.15,0.06)); d2=max(-B(p-vec2(0.,0.03),vec2(0.06,0.005)),d2); d=min(d,d2); p=pp; p-=vec2(-0.29,0.); d2=B(p,vec2(0.06,0.15)); d2=max(-B(p-vec2(0.04,0.02),vec2(0.005,0.09)),d2); d=min(d,d2); p=pp; p*=Rot(radians(-45.)); p-=vec2(-0.31,0.035); d2=B(p,vec2(0.06,0.16)); d=min(d,d2); p=pp; p*=Rot(radians(-45.)); p-=vec2(0.25,0.03); d2=B(p,vec2(0.06,0.22)); d2=max(-B(p-vec2(-0.03,-0.03),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; p-=vec2(0.29,-0.02); d2=B(p,vec2(0.06,0.105)); d=min(d,d2); p=pp; p*=Rot(radians(45.)); p-=vec2(0.31,-0.01); d2=B(p,vec2(0.06,0.2)); d=min(d,d2); p=pp; p-=vec2(-0.013,-0.29); d2=B(p,vec2(0.16,0.06)); d=min(d,d2); p=pp; p*=Rot(radians(-45.)); p-=vec2(-0.23,-0.15); d2=B(p,vec2(0.02,0.22)); d=max(-d2,d); p=pp; return max(numMask(p),d); }
        float num1(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.29,-0.29),vec2(0.06,0.18)); p-=vec2(0.06,0.08); p*=Rot(radians(-50.)); float d2=B(p,vec2(0.06,0.6)); d2=max(-B(p-vec2(0.04,0.05),vec2(0.005,0.3)),d2); d=min(d,d2); p=pp; p-=vec2(0.1,0.25); p*=Rot(radians(-50.)); d2=B(p,vec2(0.06,0.45)); d2=max(-B(p-vec2(0.04,-0.1),vec2(0.005,0.17)),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num2(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.11,0.29),vec2(0.24,0.06)); p-=vec2(-0.3,0.15); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(0.04,0.05),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; p-=vec2(0.,0.0); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.6)); d2=max(-B(p-vec2(0.04,0.05),vec2(0.005,0.3)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.11,-0.29),vec2(0.24,0.06)); d=min(d,d2); p=pp; p-=vec2(0.29,-0.15); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(-0.04,-0.03),vec2(0.005,0.12)),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num3(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.11,0.29),vec2(0.24,0.06)); p-=vec2(-0.3,0.15); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(0.04,0.05),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; p-=vec2(0.18,0.153); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.4)); d2=max(-B(p-vec2(0.04,-0.1),vec2(0.005,0.25)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.268,-0.09),vec2(0.18,0.06)); d=min(d,d2); p=pp; p-=vec2(0.3,-0.15); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.3)); d=min(d,d2); p=pp; d2=B(p-vec2(-0.11,-0.29),vec2(0.24,0.06)); float a=radians(50.); p.y+=0.52; d2=max(-dot(p,vec2(cos(a),sin(a))),d2); d=min(d,d2); p=pp; d2=B(p-vec2(0.29,0.06),vec2(0.06,0.2)); a=radians(-50.); p.x-=0.16; d2=max(-dot(p,vec2(cos(a),sin(a))),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num4(vec2 p){ vec2 pp=p; float d=B(p-vec2(-0.22,-0.06),vec2(0.18,0.06)); p-=vec2(-0.2,0.14); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.4)); d2=max(-B(p-vec2(-0.04,0.1),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; p-=vec2(0.228,0.183); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.4)); d2=max(-B(p-vec2(0.04,-0.13),vec2(0.005,0.22)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.18,-0.29),vec2(0.18,0.06)); d=min(d,d2); p=pp; p-=vec2(0.119,-0.178); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.4)); d=min(d,d2); p=pp; d2=B(p-vec2(0.29,-0.19),vec2(0.06,0.18)); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num5(vec2 p){ vec2 pp=p; float d=B(p-vec2(-0.05,0.29),vec2(0.29,0.06)); d=max(-B(p-vec2(0.05,0.25),vec2(0.15,0.005)),d); p-=vec2(0.29,0.24); float d2=B(p,vec2(0.06,0.12)); float a=radians(50.); p.y+=0.06; d2=max(-dot(p,vec2(cos(a),sin(a))),d2); d=min(d,d2); p=pp; p-=vec2(0.,0.0); p*=Rot(radians(-50.)); d2=B(p,vec2(0.06,0.6)); d2=max(-B(p-vec2(-0.04,0.05),vec2(0.005,0.2)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(0.11,-0.29),vec2(0.24,0.06)); d=min(d,d2); p=pp; p-=vec2(-0.29,-0.15); p*=Rot(radians(-50.)); d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(0.04,-0.05),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num6(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.18,0.0),vec2(0.185,0.06)); p-=vec2(-0.06,0.15); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.5)); d2=max(-B(p-vec2(-0.04,-0.05),vec2(0.005,0.25)),d2); d=min(d,d2); p=pp; p-=vec2(-0.198,-0.18); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.303)); d2=max(-B(p-vec2(-0.04,0.1),vec2(0.005,0.12)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.18,-0.29),vec2(0.24,0.06)); d=min(d,d2); p=pp; p-=vec2(0.23,-0.15); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(0.04,-0.05),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num7(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.11,0.29),vec2(0.24,0.06)); p-=vec2(-0.3,0.15); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.3)); d=min(d,d2); p=pp; p-=vec2(0.,0.0); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.6)); d2=max(-B(p-vec2(-0.04,-0.05),vec2(0.005,0.3)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.17,-0.29),vec2(0.18,0.06)); float a=radians(-50.); p.x-=0.24; d2=max(dot(p,vec2(cos(a),sin(a))),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num8(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.11,0.29),vec2(0.24,0.06)); p-=vec2(-0.3,0.15); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.3)); d=min(d,d2); p=pp; p-=vec2(0.24,0.188); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(-0.04,-0.12),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.18,0.01),vec2(0.23,0.06)); d=min(d,d2); p=pp; p-=vec2(0.04,-0.178); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.5)); d2=max(-B(p-vec2(-0.04,0.15),vec2(0.005,0.2)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(0.14,-0.29),vec2(0.24,0.06)); d=min(d,d2); d2=B(p-vec2(0.29,-0.23),vec2(0.06,0.24)); d=min(d,d2); p=pp; return max(numMask(p),d); }
        float num9(vec2 p){ vec2 pp=p; float d=B(p-vec2(0.11,0.29),vec2(0.24,0.06)); p-=vec2(-0.3,0.15); p*=Rot(radians(50.)); float d2=B(p,vec2(0.06,0.3)); d=min(d,d2); p=pp; p-=vec2(0.24,0.188); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.3)); d2=max(-B(p-vec2(-0.04,-0.12),vec2(0.005,0.1)),d2); d=min(d,d2); p=pp; d2=B(p-vec2(-0.18,0.01),vec2(0.23,0.06)); d=min(d,d2); p=pp; p-=vec2(0.04,-0.178); p*=Rot(radians(50.)); d2=B(p,vec2(0.06,0.5)); d2=max(-B(p-vec2(-0.04,0.08),vec2(0.005,0.2)),d2); d=min(d,d2); p=pp; return max(numMask(p),d); }

        float drawFont(vec2 p, int char_val){
            if(char_val==0) return num0(p); if(char_val==1) return num1(p); if(char_val==2) return num2(p);
            if(char_val==3) return num3(p); if(char_val==4) return num4(p); if(char_val==5) return num5(p);
            if(char_val==6) return num6(p); if(char_val==7) return num7(p); if(char_val==8) return num8(p);
            if(char_val==9) return num9(p); return 1.0;
        }

        float drawNumber(vec2 p){
            vec2 prevP = p;
            p *= 2.0;
            
            float duration = 1.0;
            float progress = clamp(iTime / duration, 0.0, 1.0);
            int val = int(floor(progress * 99.0));
            
            int tens = val / 10;
            int ones = int(mod(float(val), 10.0));
            
            float d = drawFont(p - vec2(-0.37, 0.0), tens);
            float d2 = drawFont(p - vec2(0.37, 0.0), ones);
            d = min(d, d2);
            
            p = prevP;
            float box = abs(B(p, vec2(0.4, 0.22))) - 0.005;
            box = max(-(abs(p.x) - 0.36), box);
            box = max(-(abs(p.y) - 0.18), box);
            return min(d, box);
        }

        float arrow(vec2 p){float d=Tri(p,vec2(50.));p-=vec2(0.,-25.);float d2=Tri(p,vec2(50.));return max(-d2,d);}
        float drawArrow(vec2 p){p*=200.;p.y-=iTime*20.;p.y=mod(p.y,50.)-25.;p.y-=25.;float d=arrow(p);float mask=arrow(p);d=max(mask,d);float d2=abs(arrow(p))-0.5;return min(d,d2);}
        float bgArrow(vec2 p){vec2 prevP=p;p.y+=0.06-iTime*0.1;p.y=mod(p.y,0.12)-0.06;vec2 subP=p;p.y-=0.05;p.x*=1.5;float d=Tri(p,vec2(0.012));p=subP;float d2=B(p,vec2(0.001,0.05));return min(d,d2);}
        float drawBg(vec2 p){vec2 prevP=p;p.x=mod(p.x,0.24)-0.12;p.y=mod(p.y,0.12)-0.06;float d=bgArrow(p);p=prevP;p.x+=0.12;p.x=mod(p.x,0.24)-0.12;p.y=mod(p.y,0.12)-0.06;p.y*=-1.;d=min(d,bgArrow(p));p=prevP;p.x=mod(p.x,0.12)-0.06;p.y=mod(p.y,0.24)-0.12;vec2 p_rot=p*Rot(radians(90.0));d=min(d,bgArrow(p_rot));p=prevP;p.y+=0.12;p.x=mod(p.x,0.12)-0.06;p.y=mod(p.y,0.24)-0.12;p*=Rot(radians(-90.0));d=min(d,bgArrow(p));return d;}
        float drawItems(vec2 p){vec2 prevP=p;p.y-=iTime*0.2;p.y=mod(p.y,0.2)-0.1;p*=Rot(radians(45.0));float d=abs(B(p,vec2(0.02)))-0.003;p=prevP;p.y+=0.1;p.y-=iTime*0.2;p.y=mod(p.y,0.2)-0.1;float d2=min(B(p,vec2(0.003,0.02)),B(p,vec2(0.02,0.003)));return min(d,d2);}
        float mainVisual(vec2 p){vec2 prevP=p;vec2 puv=PUV(p);puv*=0.47;puv.x-=iTime*0.1;puv=mod(puv,0.5)-0.25;vec2 p_rot=vec2(puv.y,-puv.x);p_rot.x*=1.5;float d=drawArrow(p_rot);p=prevP;float ang=atan(p.y,p.x);float len=length(p);float seg=6.28/(3.*8.);float mod_ang=mod(ang+seg,6.28/((3.*8.)*0.5));p=len*cos(mod_ang+(3.-1.)*seg+vec2(0.,11.));p=abs(p)-0.1;p*=Rot(radians(45.));float d2=drawItems(p);p=prevP;d2=max(-(abs(p.x)-0.05),d2);p*=Rot(radians(60.));d2=max(-(abs(p.x)-0.05),d2);p=prevP;p*=Rot(radians(-60.));d2=max(-(abs(p.x)-0.05),d2);d=min(d,d2);return d;}
        float uiItem0(vec2 p){float d=abs(B(p,vec2(0.05)))-0.003;d=max(-(abs(p.x)-0.035),d);d=max(-(abs(p.y)-0.035),d);p*=Rot(radians(45.));float d2=min(B(p,vec2(0.003,0.04)),B(p,vec2(0.04,0.003)));return min(d,d2);}
        float drawUI(vec2 p){vec2 prevP=p;p.x+=0.6;p.y+=0.36;float d=uiItem0(p);p.x=abs(p.x)-0.12;float d2=uiItem0(p);d=min(d,d2);p=prevP;p.x-=0.6;p.y-=0.36;d2=uiItem0(p);d=min(d,d2);p.x=abs(p.x)-0.12;d2=uiItem0(p);d=min(d,d2);p=prevP;p.y=abs(p.y)-0.25;p.y*=-1.;d2=Tri(p,vec2(0.02));d=min(d,d2);return d;}
    """

    HUD_MAIN_CODE = """
        iTime = u_anim_time;
        
        vec2 fragCoord = v_tex_coord * u_model_size;
        vec2 iResolution = u_model_size;
        vec2 uv = (fragCoord - 0.5 * iResolution.xy) / iResolution.y;
        
        uv.y = -uv.y; 
        
        vec3 col = vec3(0.0);
        
        float d = drawBg(uv);
        col = mix(col, vec3(0.3), S(d, 0.0, iResolution));
        
        d = mainVisual(uv);
        col = mix(col, vec3(0.5), S(d, 0.0, iResolution));
        
        col *= length(uv) - 0.1;
        
        d = drawNumber(uv);
        col = mix(col, vec3(1.0), S(d, 0.0, iResolution));
        
        d = drawUI(uv);
        col = mix(col, vec3(1.0), S(d, 0.0, iResolution));
        
        gl_FragColor = vec4(sqrt(col), 1.0);
    """

    renpy.register_shader("shadertoy.SciFiHUDComplete", variables="""
        uniform vec2 u_model_size;
        uniform float u_anim_time;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions=HUD_FUNCTIONS,
    fragment_300=HUD_MAIN_CODE)



image hud:
    "eatingstreet"
    
    shader "shadertoy.SciFiHUDComplete"
    
    u_anim_time 0.0
    linear 1000.0 u_anim_time 1000.0